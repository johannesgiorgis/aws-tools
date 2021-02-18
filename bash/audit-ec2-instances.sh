#!/usr/bin/env bash

# Audit EC2 Instances - Get list of EC2 Instances across all regions


function main() {
    # default values
    PROFILE="--profile default"

    options='p:'
    while getopts $options opt; do
        case "$opt" in
            p) PROFILE="--profile $OPTARG" ;;
            :) echo "Option -$OPTARG requires an argument." >&2; usage; exit 1 ;;
            \?) echo "Invalid option: -$OPTARG" >&2; usage; exit 1 ;;
        esac
    done
    shift $((OPTIND-1))

    check_dependencies_present

    regions=$(aws ec2 describe-regions | jq -r '.Regions[].RegionName' | sort)
    num_regions=$(echo "$regions" | wc -l | sed 's/ //g')

    header="instance_id,instance_type,instance_name,state,key_name,launch_time"
    all_instances_details=""
    count=1
    for region in $regions; do
        echo "$count/$num_regions - Checking region '$region'..."
        REGION="--region $region"
        result=$(ec2 describe-instances)
        num_instances=$(echo "$result" | grep 'InstanceId' | wc -l | sed 's/ //g')

        all_instances_details="${all_instances_details}REGION:${region} - ${num_instances} instances\n"
        if [[ $num_instances > 0 ]]; then
            region_instances_details=$(echo "$result" | jq -r \
                '.Reservations[].Instances[]
                | [ .InstanceId, .InstanceType, (.Tags[]? | if .Key == "Name" then .Value else empty end) // "", .State.Name, .KeyName, .LaunchTime ]
                | @csv')
            all_instances_details="${all_instances_details}${header}\n${region_instances_details}\n"
        fi
        ((count++))
    done

    echo -e "\nAll Instances Details"
    echo -e "$all_instances_details"
}


function usage() {
    echo "ERROR: Script requires the following inputs:"
    echo "Usage:"
    echo -e "\t$0 -p <aws-profile:default>"
    echo -e "\t$0 -p default"
}


function check_dependencies_present() {
    # require jq, aws be installed
    if ! which jq > /dev/null 2>&1; then echo "The 'jq' command is not installed, aborting." >&2; exit; fi
    if ! which aws > /dev/null 2>&1; then echo "The 'aws' command is not installed, aborting." >&2; exit; fi
}


function setval { printf -v "$1" "%s" "$(cat)"; declare -p "$1"; }


function myaws () {
    aws $PROFILE $REGION "$@"
}

function ec2 () { myaws ec2 "$@"; }

main "$@"
