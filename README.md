# English Sentiment Analysis Lab

An educational Python application for exploring the polarity of English text. A Streamlit interface uses **TextBlob's built-in sentiment analyzer** to display a positive, negative, or neutral result. This project does not train or fine-tune a custom machine-learning model.

## Features and stack

- Analyze English text on demand, without an API key or hosted inference service.
- View polarity from `-1` to `1`, rounded to two decimal places for display. Classification uses the original score: above zero is positive, below zero is negative, and zero is neutral.
- Warn about blank input and display a safe error if analysis is unavailable.
- Exercise behavior with unit tests, opt-in real-library tests, and a container health check.

**Stack:** Python 3.11, Streamlit, TextBlob, Docker, and GitHub Actions. Python 3.11 is the intended application/container baseline; dependency-free tests also run on Python 3.14. No corpus download is expected for the default polarity analyzer.

## Installation and local execution

From the repository root:

```sh
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.address=127.0.0.1 --browser.gatherUsageStats=false
```

Open `http://localhost:8501`, enter English text, and click **Analyze**. Stop with Ctrl+C. Try `I love this wonderful day`, `I hate this terrible day`, and `table`.

Installation downloads Streamlit, TextBlob, and their transitive dependencies. Requirements currently remain unpinned: a tested dependency lock and immutable image/action references are follow-up work. Record resolved versions after successful verification with `python -m pip freeze`; do not treat untested version pins as a verified lock.

## Docker

Building may download the Python base image and installs the requirements:

```sh
docker build -t ai-sentiment-lab:local .
docker run --rm --name sentiment-lab -p 127.0.0.1:8501:8501 ai-sentiment-lab:local
```

Open `http://localhost:8501`. The host port is restricted to loopback. The image uses Python 3.11 slim, copies only application files, disables telemetry, and runs as non-root `appuser` (UID 10001). Stop with Ctrl+C; `--rm` removes the container.

From another terminal, inspect startup and readiness:

```sh
docker logs sentiment-lab
docker inspect --format '{{.State.Health.Status}}' sentiment-lab
curl --fail --max-time 5 http://127.0.0.1:8501/_stcore/health
```

The health endpoint checks service readiness; it does not establish sentiment accuracy or exercise every UI interaction.

## Testing

Run from the repository root. The default suite uses only the Python standard library:

```sh
python3 -B -m unittest discover -s tests -v
```

There are **14 dependency-free tests** and **3 opt-in dependency-backed tests**. Unit tests cover polarity boundaries and invalid scores, blank input, analyzer delegation/failure, and UI branches using a fake Streamlit module. They do not establish real NLP behavior or browser rendering.

After installing the requirements in the virtual environment, enable integration checks:

```sh
RUN_DEPENDENCY_TESTS=1 python -B -m unittest discover -s tests -v
```

These use real TextBlob examples and Streamlit AppTest for positive, negative, neutral, and blank-input behavior. Missing or broken dependencies fail explicitly when enabled. AppTest does not replace a browser smoke test.

Alternatively, run the full suite in a built image, mounting tests read-only:

```sh
docker run --rm --entrypoint python \
  --mount "type=bind,source=$PWD/tests,target=/app/tests,readonly" \
  -e RUN_DEPENDENCY_TESTS=1 \
  ai-sentiment-lab:local -B -m unittest discover -s tests -v
```

## Project structure

```text
app.py                      Streamlit interface and safe error presentation
sentiment.py                TextBlob adapter and polarity classification
requirements.txt            Application dependencies
Dockerfile                  Non-root runtime and HTTP health check
.dockerignore               Excludes Git, credentials, caches, tests, and docs
tests/test_sentiment.py     Dependency-free analysis checks
tests/test_app.py           Dependency-free UI contract checks
tests/test_dependencies.py  Opt-in real-library checks
.github/workflows/ci.yml    Tests, image build, and health verification
```

## Continuous integration

The workflow runs on pushes to `main` and `portfolio/**`, and pull requests targeting `main`. It uses read-only repository permissions and checkout without persisted credentials. It runs unit tests, builds the image, exercises real dependencies inside it, and checks container health with a bounded wait. Failure diagnostics and container cleanup are included. No secrets, paid services, deployment, or registry publication are required.

## Limitations and verification status

- Polarity is not confidence, intent detection, or fact checking. Sarcasm, mixed emotions, slang, and specialized language may produce misleading results.
- The UI requests English but does not detect language. There is no labeled evaluation dataset or measured accuracy claim.
- This is a learning application without persistence, authentication, a production serving assessment, or a custom model.
- Local dependency-free tests pass. Real-library tests, application startup, Docker build/health, and hosted CI remain unverified in the preparation environment: packages are absent, network access is blocked, and Docker daemon access is denied. No successful container or deployment result is claimed.
- Dependencies and image/action tags are not immutable. Resolve and verify them in a permitted environment before relying on reproducible builds or publishing security claims.

References: [Streamlit Docker guide](https://docs.streamlit.io/deploy/tutorials/docker), [Streamlit application testing](https://docs.streamlit.io/develop/concepts/app-testing/get-started), and [TextBlob documentation](https://textblob.readthedocs.io/en/dev/).
