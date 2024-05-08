# ASAM ODS EXD-API IMCtermite plugin

This repository contains a [ASAM ODS EXD-API](https://www.asam.net/standards/detail/ods/) plugin that uses [IMCtermite](https://pypi.org/project/IMCtermite/) to read .raw files of [imc Software](https://www.imc-tm.de/).

> This is only a prototype to check if it works with [IMCtermite](https://github.com/RecordEvolution/IMCtermite/).


## GRPC stub

Because the repository does not contain the [ASAM ODS](https://www.asam.net/standards/detail/ods/) protobuf files the generated stubs are added.
The files that match `*_pb2*` are generated suing the following command. To renew them you must put the 
proto files from the ODS standard into `proto_src` and rerun the command.

```
python -m grpc_tools.protoc --proto_path=proto_src --pyi_out=. --python_out=. --grpc_python_out=. ods.proto ods_external_data.proto
```

## Content

### `exd_api_server.py`

Runs the GRPC service to be accessed using http-2.

### `external_data_reader.py`

Implements the EXD-API interface to access IMC Bus Format (*.raw, *.dat) files using [IMCtermite](https://github.com/RecordEvolution/IMCtermite/).

### `exd_api_test.py`

Some basic tests on example files in `data` folder.

### `example_access_exd_api_IMCtermite.ipynb`

jupyter notebook the shows communication done by ASAM ODS server or Importer using the EXD-API plugin.