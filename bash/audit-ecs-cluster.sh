#!/usr/bin/env bash

# Audit ECS Clusters - Get list of ECS Clusters across all regions


function main() {
    # default values
    PROFILE="--profile default"

    options='p:v'
    while getopts $options opt; do
        case "$opt" in
            p) PROFILE="--profile $OPTARG" ;;
            v) VERBOSE=1 ;;
            :) echo "Option -$OPTARG requires an argument." >&2; usage; exit 1 ;;
            \?) echo "Invalid option: -$OPTARG" >&2; usage; exit 1 ;;
        esac
    done
    shift $((OPTIND-1))

    check_dependencies_present

    regions=$(aws ec2 describe-regions | jq -r '.Regions[].RegionName' | sort)
    num_regions=$(echo "$regions" | wc -l | sed 's/ //g')

    header="instance_id,instance_type,instance_name,state,key_name,launch_time"
    all_clusters_details=""
    all_clusters_summary=""
    count=1
    for region in $regions; do
        echo "$count/$num_regions - Checking region '$region'..."
        REGION="--region $region"
        cluster_arns=$(ecs list-clusters | jq -r '.clusterArns[]')

        if [[ $cluster_arns != "" ]]; then
            num_clusters=$(echo "$cluster_arns" | wc -l | sed 's/ //g')
        else
            num_clusters=0
        fi

        all_clusters_details="${all_clusters_details}REGION:${region} - ${num_clusters} clusters\n"
        all_clusters_summary="${all_clusters_summary}REGION:${region} - ${num_clusters} clusters\n"

        if [[ $VERBOSE == 1 ]]; then
            for cluster_arn in $cluster_arns; do
                services=$(ecs list-services --cluster $cluster_arn | jq -r '.serviceArns[]')

                if [[ $services != "" ]]; then
                    num_services=$(echo "$services" | wc -l | sed 's/ //g')
                else
                    num_services=0
                fi
                all_clusters_details="${all_clusters_details}\nCLUSTER:${cluster_arn} - ${num_services} services"
                all_clusters_details="${all_clusters_details}\n${services}\n"
            done
        fi
        ((count++))
    done

    if [[ $VERBOSE == 1 ]]; then
        echo -e "\nAll Clusters Details"
        echo -e "$all_clusters_details"
    fi
    
    echo -e "\nAll Clusters Summary"
    echo -e "$all_clusters_summary"
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

function ecs () { myaws ecs "$@"; }

main "$@"
