# whoami

A data-driven resume and CV, rendered by [Hugo](https://gohugo.io) and deployed to GitHub Pages. One set of YAML data produces two documents that share a single visual system:

| | Web | PDF |
| --- | --- | --- |
| 📘 **CV** (full record) | [rezarajan.github.io/whoami](https://rezarajan.github.io/whoami) | [cv.pdf](https://rezarajan.github.io/whoami/cv.pdf) |
| 📄 **Resume** (one page, A4) | [/resume](https://rezarajan.github.io/whoami/resume/) | [resume.pdf](https://rezarajan.github.io/whoami/resume.pdf) |

## Summary

Software engineer specializing in data systems: started in full-stack development, progressed into building end-to-end data platforms, from lakehouse architectures to their infrastructure-as-code foundations.

## Core Competencies

- **Data Engineering**: ETL/ELT, CDC, data lakehouse and modeling, Databricks, Lakebase, Trino, Airflow, dbt, Spark, PostgreSQL, AWS
- **Software Engineering**: Python, Golang, SQL, Bash, Git, CI/CD
- **Infrastructure as Code**: Kubernetes, Docker, Terraform/OpenTofu, Ansible, Nix, AWS, Azure
- **Analytics & Visualization**: Power BI, Grafana, Looker Studio

## Experience

| Organization | Role | Period |
| --- | --- | --- |
| Ministry of Education Trinidad and Tobago | Data Specialist | 2026 - Present |
| Mochi | Co-Founder / Infrastructure Engineer | Dec 2022 - Present |
| myKaarma | Data Engineer | Feb 2022 - Jan 2024 |

## Education

| Institution | Credential | Period |
| --- | --- | --- |
| UC Berkeley | Accreditation in CS (DSA) | 2025 |
| University of Waterloo | BSc. Mechanical Engineering | 2015 - 2020 |

## Certifications

- AWS Certified Data Engineer, Amazon (in progress)
- Project Initiation, Google (2026)
- Foundations of Project Management, Google (2026)
- Data Engineering with AWS, Udacity (2024)
- Self-Driving Car Engineer, Udacity (2021)
- Data Analyst, Udacity (2020)

Full details, historical roles, and course work live on the [CV](https://rezarajan.github.io/whoami).

## Repository

- Content is data: everything above renders from `hugo/data/*.yaml` into both documents.
- PDFs are build artifacts: CI prints them with headless Chrome on every deploy; nothing is tracked by hand.
- To develop locally: `git submodule update --init`, then `cd hugo && hugo server`. `scripts/generate-pdfs.sh` pre-renders the download PDFs. Versioning uses [jj](https://jj-vcs.github.io) colocated with git.
- Agent guidance (structure, conventions, quality assurance) lives in [CLAUDE.md](./CLAUDE.md).
