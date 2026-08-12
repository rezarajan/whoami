# Welcome

This repository serves as a portfolio of my professional, academic and project experiences. It uses Git to track changes over time, as well as to auto-update my resume through CI/CD workflows.

📄 [Resume](https://rezarajan.github.io/whoami/resume.pdf)

📘 [CV](https://rezarajan.github.io/whoami/cv.pdf)

👉 [Website (CV)](https://rezarajan.github.io/whoami) · [Resume page](https://rezarajan.github.io/whoami/resume/)

PDFs are generated and published by the CI/CD pipeline on every deploy; they are not tracked in the repository. For local development, `scripts/generate-pdfs.sh` pre-renders them into `hugo/static/` (gitignored) so the site's download links work locally too.

# Courses

Below are some of my courses, which showcase different competencies through projects.

| Course                                                                                   | Projects                                                                                                                  | Skills                                                                                       | Year |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ---- |
| [Data Engineering Nanodegree](https://github.com/rezarajan/udacity-aws-data-engineering) | Data Modelling with Apache Cassandra, Data Warehosue, Data Lakehouse, Data Pipelines                                      | SQL, NoSQL, Python, AWS Redshift, AWS Glue, PySpark, Data Lakehouse, Apache Airflow, ETL/ELT | 2024 |
| [Self-Driving Car Nanodegree](https://github.com/rezarajan/sdc-capstone)                 | Simulation of an Autonomous Vehicle, Traffic Sign Classifier, Extended Kalman Filters, Path Planning, Lane Line Detection | Python, C++ Tensorflow, ROS, OpenCV                                                          | 2021 |
| Data Analyst Nanodegree                                                                  | Exploratory Data Analysis, A/B Testing                                                                                    | Python, scikit, Pandas, NumPy                                                                | 2020 |

# Projects

Most of my time is spent working on projects - both in production and hobbyist. These projects help me stay engaged with the latest technology developments, as well as gain a working understanding of their implications in a real-world environment.

| Project                                                     | Description                                                                                                                                                                                                                                                                                     | Skillsets                                      |
| ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| [dotfiles](https://github.com/rezarajan/dotfiles)           | A collection of my Linux configurations, mostly focused on Nix. It helps me learn which tools are the most effective at bootstrapping Linux systems from scratch, and the drawbacks of each.                                                                                                    | Infrastructure-as-Code (IAC), Linux, Nix, Bash |
| [mbok](https://github.com/mochipool/mbok)                   | Internal documentation for Mochi, a Web3 project. This project has helped me learn what constitutes good technical documentation, and how to share that among stakeholders effectively.                                                                                                         | Hugo, GitHub Actions (CI/CD)                   |
| [mainline (private)](https://github.com/mochipool/mainline) | This repository contains source code for microservices run in the Mochi project. Microservices are usually written in Golang, development environments created with Nix, containerized build systems run with Earthly, and deployments done using Kustomize or Flux across Kubernetes clusters. | Kubernetes, Golang, Nix, Podman, Earthly (CD)  |

