BEGIN {
    myaccount="thrivent"
    myaccount="thrivent_match"
    symbol="aasmx"
    FS="\t"
    print "account,date,symbol,shares,price,type,note"
}

FNR==1 {
    if(match($1, "Description")){
        next
    }
}

FNR >= 1 {
    # Reset variables
    mydate=""
    note=""
    type=""

    # Parse the date into my format
    parsedate="date --date="$2" +%Y%m%d"
    parsedate | getline mydate
    close(parsedate)

    # Remove dollar sign from price
    sub(/\$/, "", $4)
    # Trim whitespace from price
    sub(/ /, "", $4)

    # Determine transaction type
    if(match($1, /CANCEL|DECREASE|CNCL|FEE/)){
        shares=-$3
    } else {
        shares=$3
    }
    # Trim whitespace from shares
    sub(/ /, "", $3)

    # Determine type and note
    if(match($1, /EMPLOYER CONTRIB/)){
        type="purchase"
        note="employer_contribution"
    } else if(match($1, /FEE/)){
        type="fee"
        note=""
    } else if(match($1, /DECREASE|CANCELLATION/)){
        type="cancellation"
        note="employer_correction"
    } else if(match($1, /CNCL EE CONTR/)){
        type="cancellation"
        note="employer_correction"
    } else if(match($1, /SALARY REDUCTION CONT/)){
        type="purchase"
        note=""
    } else if(match($1, /EE SAL RED/)){
        type="purchase"
        note=""
    } else if(match($1, /DIV REINVESTED/)){
        type="div_reinvest"
        note=""
    } else if(match($1, /SHRTTERM CG REIN/)){
        type="cg_reinvest"
        note="short_term_cap_gain"
    } else if(match($1, /L\/T CP GAIN REIN/)){
        type="cg_reinvest"
        note="long_term_cap_gain"
    } else if(match($1, /INCREASE DIVIDEND PAYMENT/)){
        type="div_reinvest"
        note=""
    } else if(match($1, /INCREASE SHORT TERM CAP GN/)){
        type="cg_reinvest"
        note="short_term_cap_gain"
    } else if(match($1, /INCREASE CAP GAIN PAYMENT/)){
        type="cg_reinvest"
        note="cap_gain"
    } 

    print myaccount","mydate","symbol","$3","$4","type","note
    #print "thrivent_match,"mydate","symbol","$3","$4","type","note
}
