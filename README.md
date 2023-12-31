# Clean Room

Data Clean Room utilities for probabilistic information exchange.



## Installation

1. Download the repo: https://github.com/mobarski/cleanroom-test/archive/refs/heads/main.zip

2. Unzip the file to a new directory.

3. Use the executable file specific to your operating system:

   - linux: cleanroom

   - windows: cleanroom.exe

   - ~~macos: cleanroom-macos~~



## Basic Usage



#### print help

`cleanroom --help`

output:

```
    data clean room utility for anonymous intersection of sets

    USAGE:  model  create|intersect  model_path  [options]

    OPTIONS:
        -i  --input   path  = stdin
        -o  --output  path
        -r  --real    path
        -k  --keys    path
            --error   float = 0.05
            --error2  float = 0.0001
            --version


    Copyright (c) 2023 Maciej Obarski
    Free for non-commercial and commercial non-production use.
    Commercial production use requires written permission.

```



#### create model

`cleanroom create my.model -i data.txt`

- `data.txt` - input text file with a single column containing entity identifiers (IPs, emails, cookies, etc), one id per line, no header
- `my.model` - cleanroom model created by this step (binary file)

example output:

```
    # model: my.model
    - input items: ~10.0k
    - model items: ~9.5k
    - bits per item: 19.1
    - size: ~22.7kb
    - keys: 13
    - desired error: 5.0%
    - minimal error: 0.0102%

    # model processing:
      Time: 11.4 ms
      Rate: 0.9M items/s
      Runs: 1

    Copyright (c) 2023 Maciej Obarski
    Free for non-commercial and commercial non-production use.
    Commercial production use requires written permission.
```



#### intersect

`cleanroom intersect my.model -i other.txt -o common.txt`

- `other.txt` - input text file with a single column containing entity identifiers (IPs, emails, cookies, etc), one id per line, no header

- `common.txt` - output text file that contains identifiers common to my.model and other.txt file, one id per line, no header

example output:

```
    model intersection:     815 (0.8% of 100000 input ids)
    # model processing:
      Time: 70.0 ms
      Rate: 1.4M items/s
      Runs: 1

    Copyright (c) 2023 Maciej Obarski
    Free for non-commercial and commercial non-production use.
    Commercial production use requires written permission.
```





## Test script usage

- before running the test script:

  - install required python modules:
    - `pip install -r requirements.txt`

- edit the `test` script to configure the parameters:

  ```
  A = number of items in the A set
  B = number of items in the B set
  C = number of common items in A and B
  N = number of unique IDs to generate if the IDs are not already generated
  kind = faker method to use for generating IDs:
      ipv4, ipv6, email, mac_address, vin, iban, slug, etc.
  ```

- run the `test` script

  - first run with the new `kind` of ID might take around 1 minute  as the system is creating the pool of 2_000_000 unique IDs

  - following runs should take single seconds

  - example output:

    ```
    loaded ipv4 IDs: 2000000
    shuffling A and B
    saving work/A.txt
    saving work/B.txt
    saving work/AH.txt
    saving work/BH.txt
    DONE
    
    # model: work/mm
    - input items: ~100.0k
    - model items: ~80.0k
    - bits per item: 19.1
    - size: ~191.4kb
    - keys: 13
    - desired error: 20.0%
    - minimal error: 0.0102%
    
    # model processing:
      Time: 66.8 ms
      Rate: 1.5M items/s
      Runs: 1
    
    Copyright (c) 2023 Maciej Obarski
    Free for non-commercial and commercial non-production use.
    Commercial production use requires written permission.
    
    
    model intersection:   77467 (7.7% of 1000000 input ids)
    real intersection:    80000
    true positives:       64244
    
    false positives:      13223   16.5% vs real  intersection
    false negatives:      15756   19.7% vs real  intersection
    false items:          28979   36.2% vs real  intersection
                                  37.4% vs model intersection
                                   2.9% vs input size (1000000)
                                  29.0% vs real  size (100000)
    # model processing:
      Time: 1.5 s
      Rate: 0.7M items/s
      Runs: 1
    
    Copyright (c) 2023 Maciej Obarski
    Free for non-commercial and commercial non-production use.
    Commercial production use requires written permission.
    ```



## Advanced Usage



#### check intersection

`cleanroom intersect my.model -i other.txt`

example output: SAME AS ABOVE BUT `common.txt` IS NOT CREATED



#### test intersection

`cleanroom intersect my.model -i other.txt -r data.txt`

- `data.txt` - the same text file that was used to build the model

example output:

```
    model intersection:     815 (0.8% of 100000 input ids)
    real intersection:      800
    true positives:         767

    false positives:         48    6.0% vs real  intersection
    false negatives:         33    4.1% vs real  intersection
    false items:             81   10.1% vs real  intersection
                                   9.9% vs model intersection
                                   0.1% vs input size (100000)
                                   0.8% vs real  size (10000)
    # model processing:
      Time: 87.5 ms
      Rate: 1.1M items/s
      Runs: 1

    Copyright (c) 2023 Maciej Obarski
    Free for non-commercial and commercial non-production use.
    Commercial production use requires written permission.

```



#### create model with custom error level (30%)

`cleanroom create my.model -i data.txt --error 0.3`



#### create model and generate model protection keys

`cleanroom create my.model -i data.txt -k keys.txt`

- keys.txt - output text file containing random keys required for using the model (without them the model will give random results)



#### check intersection using model protection keys

`cleanroom intersect my.model -k keys.txt -i other.txt`

example output:

```
    model intersection:     809 (0.8% of 100000 input ids)
    # model processing:
      Time: 70.0 ms
      Rate: 1.4M items/s
      Runs: 1

    Copyright (c) 2023 Maciej Obarski
    Free for non-commercial and commercial non-production use.
    Commercial production use requires written permission.
```

output from the same model but without using keys:

`cleanroom intersect my.model -i other.txt`

```
    model intersection:       7 (0.0% of 100000 input ids)
    # model processing:
      Time: 57.5 ms
      Rate: 1.7M items/s
      Runs: 1

    Copyright (c) 2023 Maciej Obarski
    Free for non-commercial and commercial non-production use.
    Commercial production use requires written permission.
```





## Change log

**0.6.4** - test script documentation, automatic initialization of the test set generator

**0.6.4** - initial binary version (expires 2024-01-01)
