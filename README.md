# ASAM ODS EXD-API IMCtermite plugin

This repository contains a [ASAM ODS EXD-API](https://www.asam.net/standards/detail/ods/) plugin that uses [IMCtermite](https://pypi.org/project/IMCtermite/) to read .raw files of [imc Software](https://www.imc-tm.de/). To implement the plugin [ods_exd_api_box](https://github.com/totonga/ods-exd-api-box) is used.

## Content


### `external_data_file.py`

Implements the EXD-API interface to access IMC Bus Format (*.raw, *.dat) files using [IMCtermite](https://github.com/RecordEvolution/IMCtermite/).

### `example_access_exd_api_IMCtermite.ipynb`

jupyter notebook the shows communication done by ASAM ODS server or Importer using the EXD-API plugin.

## Docker

### Docker Image Details

The Docker image for this project is available at:

`ghcr.io/totonga/asam-ods-exd-api-imc-termite:latest`

This image is automatically built and pushed via a GitHub Actions workflow. To pull and run the image:

```
docker pull ghcr.io/totonga/asam-ods-exd-api-imc-termite:latest
docker run -v /path/to/local/data:/data -p 50051:50051 ghcr.io/totonga/asam-ods-exd-api-imc-termite:latest
```

### Using the Docker Container

To build the Docker image locally:
```
docker build -t asam-ods-exd-api-imc-termite .
```

To start the Docker container:
```
docker run -v /path/to/local/data:/data -p 50051:50051 asam-ods-exd-api-imc-termite
```