#!/usr/bin/env bash

# Audit RDS Instances - Get list of RDS Instances across all regions


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

    header="instance_identifier,instance_class,instance_creation_time,publicly_accessible"
    all_rds_instances_details=""
    count=1
    echo 'hello'
    for region in $regions; do
        echo "$count/$num_regions - Checking region '$region'..."
        REGION="--region $region"
        db_instances=$(rds describe-db-instances)
        num_instances=$(echo "$db_instances" | grep "DBInstanceIdentifier" | wc -l | sed 's/ //g')

        all_rds_instances_details="${all_rds_instances_details}REGION:${region} - ${num_instances} instances\n"
        if [[ $num_instances > 0 ]]; then
            region_db_instances_details=$(echo "$db_instances" | jq -r \
                '.DBInstances[]
                | [ .DBInstanceIdentifier, .DBInstanceClass, .InstanceCreateTime, .PubliclyAccessible ]
                | @csv')
            all_rds_instances_details="${all_rds_instances_details}${header}\n${region_db_instances_details}\n"
        fi
        ((count++))
    done

    echo -e "\nAll RDS Instances Details"
    echo -e "$all_rds_instances_details"
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

function rds () { myaws rds "$@"; }

main "$@"
