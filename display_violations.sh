#!/bin/bash

# Read JSON input from stdin and extract total_violations
#total_violations=$(jq -r '.total_violations' -)
# Print header with total_violations
printf "%-20s | %-10s | %-10s | %-30s | %-10s | %-s\n" "total_violations" "severity" "type" "infected_components" "issue_id" "violation_details_url"

# Extract and format the rest of the fields for each violation
#jq -r '.violations[] | "\(.severity) | \(.type) | \(.infected_components[0]) | \(.issue_id) | \(.violation_details_url)"' - | while IFS="|" read -r severity type infected_components issue_id violation_details_url; do
# Extract and format the rest of the fields for each violation
jq -r '.violations[] | "\(.severity) | \(.type) | \(.infected_components | join(", ")) | \(.issue_id) | \(.violation_details_url)"' - | while IFS="|" read -r severity type infected_components issue_id violation_details_url; do

    # Format extracted fields into a tabular form for each violation
    #printf "%-20s | %-10s | %-10s | %-30s | %-10s | %-s\n" "$total_violations" "$severity" "$type" "$infected_components" "$issue_id" "$violation_details_url"
    printf "%-20s | %-10s | %-10s | %-30s | %-10s | %-s\n" "$total_violations" "$severity" "$type" "$infected_components" "$issue_id" "$violation_details_url"
done
