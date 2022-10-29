BEGIN {
    FS=","
    print "account,date,symbol,shares,price,type,note"
}

FNR > 1 {
    # Reset variables
    myaccount=""
    mydate=""
    mysymbol=""
    note=""
    type=""

    # If blank line, go to next
    if(match($0, /^$/))
    {
        next
    }

    # Determine account
    if($4=="\"Thrift Savings Plan - Civilian\"")
    {
        myaccount="tsp_civ"
    }
    if($4=="\"Thrift Savings Plan - Uniformed Services\"")
    {
        myaccount="tsp_mil"
    }

    # Parse the date into my format
    gsub("\"", "", $1)
    split($1, date_parts, "-")
    mydate=date_parts[3]date_parts[1]date_parts[2]

    # Determine symbol
    if($6=="\"C Fund\"")
    {
        mysymbol="tsp_c_fund"
    }
    if($6=="\"G Fund\"")
    {
        mysymbol="tsp_g_fund"
    }
    if($6=="\"I Fund\"")
    {
        mysymbol="tsp_i_fund"
    }
    if($6=="\"S Fund\"")
    {
        mysymbol="tsp_s_fund"
    }
    if($6=="\"L 2045\"")
    {
        mysymbol="tsp_l2045"
    }
    if($6=="\"L 2050\"")
    {
        mysymbol="tsp_l2050"
    }

    # Remove quotes from price
    gsub("\"", "", $8)

    # Remove quotes from shares
    gsub("\"", "", $9)

    # Determine transaction type
    type="purchase"

    # Determine type and note
    if(match($5, /Automatic/)){
        note="employer_contribution"
    } else if(match($5, /Match/)){
        note="employer_contribution"
    }

    # Print the line
    print myaccount","mydate","mysymbol","$9","$8","type","note
}
