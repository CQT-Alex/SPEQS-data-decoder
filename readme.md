# Where to find the script
The decoder script `decode-SPEQS.py` is in the folder `pydecoder/` under this project


# Usages

```
python3 decode-SPEQS.py [-h] -inp INPUT_FILE_NAME [-a] [-s] [-t] [-p]
```

## Arguments

```
-h, --help            show this help message and exit
-inp INPUT_FILE_NAME, --input_file_name INPUT_FILE_NAME
                        Input file name
-a                    Extract all types of data
-s                    Extract experiment data
-t                    Extract thermistor data
-p                    Extract profile data
```


## Dependencies

`python3` with libraries `numpy, pandas, json, argparse` 