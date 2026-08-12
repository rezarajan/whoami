# whoami

A data-driven resume and CV, rendered by [Hugo](https://gohugo.io) and deployed to GitHub Pages. One set of YAML data produces two documents that share a single visual system:

| | Web | PDF |
| --- | --- | --- |
| 📘 **CV** (full record) | [rezarajan.github.io/whoami](https://rezarajan.github.io/whoami) | [cv.pdf](https://rezarajan.github.io/whoami/cv.pdf) |
| 📄 **Resume** (one page, A4) | [/resume](https://rezarajan.github.io/whoami/resume/) | [resume.pdf](https://rezarajan.github.io/whoami/resume.pdf) |

## How it works

- **Content is data.** Experience, education, certifications, skills, and courses live in `hugo/data/*.yaml`. Entries flagged `cv_only: true` appear on the CV but are filtered from the one-page resume; roles carry `details` (resume bullets) and optional `cv_details`/`context` (expanded CV bullets and a role description).
- **Two renderings.** The CV is the site's home page (a scrollable document with a section nav, theme slider, and in-page certificate previews); the resume renders as a fixed A4 sheet at `/resume/`. Both are Harvard-format Times New Roman with matched content styling, automatic light/dark schemes, and monotone print output.
- **PDFs are build artifacts, not tracked files.** On every push to `main`, CI builds the site, prints both pages to PDF with headless Chrome, publishes them as workflow artifacts, and deploys them with the site. Nothing to keep in sync by hand.

## Developing

```bash
git submodule update --init     # theme (once, after cloning)
cd hugo && hugo server          # http://localhost:1313
```

`scripts/generate-pdfs.sh` pre-renders `resume.pdf` and `cv.pdf` into `hugo/static/` (gitignored) so the site's download buttons also work locally.

Versioning uses [jj](https://jj-vcs.github.io) colocated with git.

## Layout

```
hugo/
  data/          experience.yaml, education.yaml, features.yaml, courses.yaml
  layouts/       home.html (CV), _default/resume.html, partials/
  assets/css/    _tokens.scss (palette), cv.scss, custom.scss, components
  static/        certificates/, favicon
.github/         build + PDF + deploy pipeline
scripts/         local PDF generation
```

## Courses

Some of my courses, which showcase different competencies through projects.

| Course | Projects | Skills | Year |
| --- | --- | --- | --- |
| [Data Engineering Nanodegree](https://github.com/rezarajan/udacity-aws-data-engineering) | Data Modelling with Apache Cassandra, Data Warehouse, Data Lakehouse, Data Pipelines | SQL, NoSQL, Python, AWS Redshift, AWS Glue, PySpark, Data Lakehouse, Apache Airflow, ETL/ELT | 2024 |
| [Self-Driving Car Nanodegree](https://github.com/rezarajan/sdc-capstone) | Simulation of an Autonomous Vehicle, Traffic Sign Classifier, Extended Kalman Filters, Path Planning, Lane Line Detection | Python, C++, TensorFlow, ROS, OpenCV | 2021 |
| Data Analyst Nanodegree | Exploratory Data Analysis, A/B Testing | Python, scikit-learn, Pandas, NumPy | 2020 |

## Projects

Most of my time is spent working on projects, both in production and hobbyist. These keep me engaged with current technology and its real-world implications.

| Project | Description | Skillsets |
| --- | --- | --- |
| [dotfiles](https://github.com/rezarajan/dotfiles) | A collection of my Linux configurations, mostly focused on Nix. It helps me learn which tools are the most effective at bootstrapping Linux systems from scratch, and the drawbacks of each. | Infrastructure-as-Code, Linux, Nix, Bash |
| [mbok](https://github.com/mochipool/mbok) | Internal documentation for Mochi, a Web3 project. This project has helped me learn what constitutes good technical documentation, and how to share it with stakeholders effectively. | Hugo, GitHub Actions (CI/CD) |
| [mainline (private)](https://github.com/mochipool/mainline) | Source code for microservices run in the Mochi project: Golang services, Nix development environments, Earthly build systems, and deployments via Kustomize/Flux across Kubernetes clusters. | Kubernetes, Golang, Nix, Podman, Earthly |
