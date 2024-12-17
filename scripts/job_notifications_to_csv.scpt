-- This script for MacOS saves info from Aquila job notifications to a CSV.
-- It works with Outlook Version 16.91. The legacy version of Outlook must be enabled
-- as the new Outlook doesn't have full support for Applescript (yet).

tell application "Microsoft Outlook"
    set targetAccount to "user@domain" -- Your target account email
    set targetSender to "aquila@quera.com" -- The sender's email address to filter
    set targetDate to date "10/11/2024" -- The date to filter messages after

    -- Get the script's directory
    set scriptFolder to (do shell script "pwd")
    set scriptFolder to POSIX file scriptFolder as text

    -- Ensure the folder path ends with a colon
    if scriptFolder does not end with ":" then
        set scriptFolder to scriptFolder & ":"
    end if

    -- Format the targetDate for the file name
    set dayString to text -2 thru -1 of ("0" & (day of targetDate as integer))
    set monthString to text -2 thru -1 of ("0" & ((month of targetDate as integer) as integer))
    set yearString to year of targetDate as string

    set dateString to dayString & "_" & monthString & "_" & yearString

    set csvFileName to "aquila_jobs_" & dateString & ".csv"
    set csvFilePath to scriptFolder & csvFileName

    log "Starting script to find emails from " & targetSender & " after " & targetDate

    -- Find the account and its inbox
    set inboxFolder to missing value
    repeat with acc in exchange accounts
        if email address of acc is targetAccount then
            set inboxFolder to inbox of acc -- Get the inbox of the account
            exit repeat
        end if
    end repeat

    -- If the account was not found
    if inboxFolder is missing value then
        log "Account not found: " & targetAccount
        return
    end if

    -- Collect data from the specified sender after the target date
    set collectedData to {} -- List to store data for CSV
    repeat with msg in (messages of inboxFolder)
        try
            -- Check if the message has a sender
            if sender of msg is not missing value then
                set senderObj to sender of msg -- Get sender object
                if address of senderObj is targetSender then
                    -- Check if the message was received after the target date
                    set receivedDate to time received of msg
                    if receivedDate > targetDate then
                        -- Get the message content
                        set msgContent to content of msg
                        -- Parse the message content to extract required information
                        set jobNumber to my extractValue(msgContent, "Job: ", "\n")
                        set resultsFile to my extractValue(msgContent, "Results file: ", "\n")
                        set jobNotes to my extractValue(msgContent, "Job notes:", "Completed time:")
                        set completedTime to my extractValue(msgContent, "Completed time: ", "\n")
                        -- Trim whitespace
                        set jobNotes to my trimText(jobNotes)
                        -- Store the data
                        set end of collectedData to {jobNumber, resultsFile, jobNotes, completedTime}
                    end if
                end if
            end if
        end try
    end repeat

    -- Write data to CSV file
    my writeDataToCSV(collectedData, csvFilePath)
    log "Data has been written to " & csvFilePath
end tell

-- Handler to extract value between a start string and end string
on extractValue(theText, startText, endText)
    set astid to AppleScript's text item delimiters
    try
        set AppleScript's text item delimiters to startText
        set theItems to text items of theText
        if (count of theItems) ≥ 2 then
            set temp to item 2 of theItems
            set AppleScript's text item delimiters to endText
            set finalItems to text items of temp
            set extractedValue to item 1 of finalItems
            set AppleScript's text item delimiters to astid
            return extractedValue
        else
            set AppleScript's text item delimiters to astid
            return ""
        end if
    on error
        set AppleScript's text item delimiters to astid
        return ""
    end try
end extractValue

-- Handler to trim whitespace
on trimText(theText)
    set theText to text of theText
    set theText to theText as string
    set astid to AppleScript's text item delimiters
    set AppleScript's text item delimiters to {" ", tab, return, linefeed}
    set theTextItems to text items of theText
    set AppleScript's text item delimiters to ""
    set trimmedText to theTextItems as string
    set AppleScript's text item delimiters to astid
    return trimmedText
end trimText

-- Handler to write data to CSV
on writeDataToCSV(dataList, filePath)
    -- Prepare CSV content with headers
    set csvContent to "Job Number,Results File,Job Notes,Completed Time\n"
    repeat with dataItem in dataList
        set {jobNumber, resultsFile, jobNotes, completedTime} to dataItem
        -- Enclose each field in double quotes to handle commas within data
        set csvLine to "\"" & jobNumber & "\",\"" & resultsFile & "\",\"" & jobNotes & "\",\"" & completedTime & "\"\n"
        set csvContent to csvContent & csvLine
    end repeat

    -- Write to file
    try
        set fileRef to open for access file filePath with write permission
        set eof of fileRef to 0 -- Clear the file before writing
        write csvContent to fileRef starting at eof
        close access fileRef
    on error errMsg
        try
            close access file filePath
        end try
        log "Error writing to file: " & errMsg
    end try
end writeDataToCSV
