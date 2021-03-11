#!/bin/bash

for form_id in `cat filenames.txt | awk -F'[/_]' '{print $5}'`
do
    curl http://0.0.0.0:5001/api/v1/store-form?form_id=${form_id}
done

