# Export Trade Data Analyzer

A Hadoop MapReduce pipeline over 600,000 real trade records from the UN Comtrade API, covering
China's exports to 216 destination countries from 2018 to 2023, with an interactive dashboard
built on the job output.

**[Live dashboard →](https://uncomtrade-bigdata.vercel.app/)**

## Pipeline

```
UN Comtrade API  →  clean_data.py  →  HDFS  →  6 MapReduce jobs  →  process_results.py  →  dashboard
   (6 requests)      normalisation            (Hadoop Streaming)      (TSV → single JSON)    (Chart.js)
```

Each job is a mapper/reducer pair in Python, run through Hadoop Streaming on a pseudo-distributed
cluster.

| Job | Question it answers | Key → value |
|---|---|---|
| 1 | Export volume by country | partner → total value, record count |
| 2 | Top products per market | (partner, HS code) → value |
| 3 | Price trends per product | (HS code, year) → avg/min/max unit price |
| 4 | Emerging markets | partner → year-over-year growth rate |
| 5 | Yearly evolution by country | (partner, year) → total value |
| 6 | Leading products per year | (year, HS code) → value |

## Results

**Job 1 — export volume.** The United States is the largest market at $1.14 trillion over the
period, followed by Hong Kong ($469B), Japan ($289B), South Korea ($242B) and Vietnam ($194B).

**Job 2 — product mix per market.** Markets differ sharply in what they buy. For the US, data
processing machines (HS 8471) lead at $154.2B, then portable computers ($128.2B) and smartphones
($80.3B). South Korea's top import is memory chips ($39B); Russia's is motor vehicles ($14.9B).

**Job 4 — emerging markets.** Among countries starting above $500M, Kyrgyzstan grew +1,239% from
2020 to 2021, followed by France (+919%) and the Netherlands (+818%) — largely post-COVID
recovery and supply-chain restructuring.

**Job 5 — yearly evolution.** US-bound exports rose from $21.6B in 2018 to a peak of $386.9B in
2022, then fell to $213.3B in 2023, tracking the pandemic electronics surge and its
normalisation.

## Repository layout

```
index.html                  the dashboard itself (Chart.js, no build step)
Code/
  data/download_comtrade.py download from the UN Comtrade API (key passed as an argument)
  data/clean_data.py        normalisation and CSV cleaning
  mapreduce/job*/           mapper.py and reducer.py for each of the six jobs
  process_results.py        merges the job TSV output into the dashboard's JSON
Report/                     project report
Presentation/               project presentation
```

The live dashboard is deployed on Vercel from
[MaximoFox487/UNCOMTRADE-BIGDATA](https://github.com/MaximoFox487/UNCOMTRADE-BIGDATA), which holds
the same `index.html`.

## Running the jobs

```bash
python3 Code/data/download_comtrade.py YOUR_COMTRADE_KEY
python3 Code/data/clean_data.py
hdfs dfs -put china_exports_clean.csv /user/input/

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files Code/mapreduce/job1_export_volume/mapper.py,Code/mapreduce/job1_export_volume/reducer.py \
  -mapper mapper.py -reducer reducer.py \
  -input /user/input/china_exports_clean.csv -output /user/output/job1
```

Repeat for each job, then run `Code/process_results.py` to merge the TSV output into the JSON the
dashboard reads. The script expects the job output under a local directory; adjust `OUTPUT_DIR` at
the top of the file to match your setup.

## Environment

Hadoop 3.3.6 in pseudo-distributed mode on Ubuntu, Java 11, Python 3, Hadoop Streaming.

## Team

Big Data Processing Technology, Beijing Institute of Technology, spring 2026.
Instructor: Prof. Meihui Zhang.

- **Máximo Fox** — system architecture, Hadoop cluster setup and HDFS configuration, data
  acquisition from the UN Comtrade API, MapReduce jobs 1, 2 and 4, results post-processing.
- **Tomás Cruz** — data cleaning pipeline, MapReduce jobs 3, 5 and 6, dashboard and Vercel
  deployment, report and presentation.
