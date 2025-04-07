import requests
from lxml import etree
import asyncio
import aiohttp
from bs4 import BeautifulSoup

def get_webenv_and_querykey(pmid_list):
    pmid_str = ",".join(map(str, pmid_list))
    epost_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/epost.fcgi?db=pubmed&id={pmid_str}&retmode=xml&version=2.0"

    response = requests.get(epost_url)
    tree = etree.fromstring(response.content)

    webenv = tree.xpath("//WebEnv/text()")
    query_key = tree.xpath("//QueryKey/text()")

    if webenv and query_key:
        return webenv[0], query_key[0]
    return None, None


def get_gds_ids(webenv, query_key):
    elink_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=gds&WebEnv={webenv}&query_key={query_key}&retmode=xml&version=2.0"

    response = requests.get(elink_url)
    tree = etree.fromstring(response.content)
    gds_ids = tree.xpath("//Link/Id/text()")

    return gds_ids


def get_summaries(gds_ids):
    all_data = {}

    BATCH_SIZE = 100               # The list is divided into smaller batches of 100 IDs each, due to the NCBI ESummary API limitation (~200 IDs per request).

    for i in range(0, len(gds_ids), BATCH_SIZE):
        batch = gds_ids[i:i + BATCH_SIZE]
        ids_str = ",".join(batch)

        esummary_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&id={ids_str}&retmode=xml&version2.0"
        response = requests.get(esummary_url)
        tree = etree.fromstring(response.content)

        titles = tree.xpath("//Item[@Name='title']/text()")
        summaries = tree.xpath("//Item[@Name='summary']/text()")
        accessions = tree.xpath("//DocSum/Item[@Name='Accession']/text()")
        organisms = tree.xpath("//Item[@Name='taxon']/text()")
        experiments_type = tree.xpath("//Item[@Name='gdsType']/text()")

        pubmed_ids = tree.xpath("//Item[@Name='PubMedIds']/Item/text()")
        counts = [len(doc.xpath(".//Item[@Name='PubMedIds']/Item")) for doc in tree.xpath("//DocSum")]

        designs = asyncio.run(get_all_overall_designs(accessions))
        #designs = asyncio.run(get_all_overall_designs_soft(accessions))

        current_index = 0
        for j, id in enumerate(batch):
            overall_design = designs[accessions[j]]
            pubmed_slice = pubmed_ids[current_index:current_index + counts[j]]
            current_index += counts[j]

            all_data[id] = {
                "pubmed_ids": pubmed_slice,
                "concat": titles[j] + " " + experiments_type[j] + " " + summaries[j] + " " + organisms[
                    j] + " " + overall_design
            }

    return all_data


async def fetch_overall_design(session, geo_id):
    url = f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={geo_id}"
    async with session.get(url) as response:
        text = await response.text()
        soup = BeautifulSoup(text, "html.parser")

        rows = soup.find_all("tr", {"valign": "top"})
        for row in rows:
            cells = row.find_all("td")
            if len(cells) == 2:
                header_text = cells[0].get_text(strip=True)
                if "Overall design" in header_text:
                    overall_design = cells[1].get_text(separator="\n", strip=True)
                    return geo_id, overall_design
        return geo_id, ""


async def get_all_overall_designs(geo_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_overall_design(session, geo_id) for geo_id in geo_ids]
        results = await asyncio.gather(*tasks)
        return dict(results)



async def get_all_overall_designs_soft(geo_ids):                                        # Another method for retrieving Overall design, parsing the SOFT file.
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_overall_design_soft(session, geo_id) for geo_id in geo_ids]
        results = await asyncio.gather(*tasks)
        return dict(results)


async def fetch_overall_design_soft(session, geo_id):

    url = f"https://ftp.ncbi.nlm.nih.gov/geo/series/{geo_id[:6]}nnn/{geo_id}/soft/{geo_id}_family.soft.gz"

    async with session.get(url) as response:

        overall_design = None

        async for line in response.content.iter_any():
            decoded_line = line.decode("utf-8", errors="ignore")
            if "!Series_overall_design" in decoded_line:
                overall_design = decoded_line.split("= ", 1)[1]
                break

        return geo_id, overall_design