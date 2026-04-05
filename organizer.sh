#!/usr/bin/env bash
# =============================================================================
#
#   Archive the current grades.csv with a timestamp, reset the workspace
#   with a fresh empty grades.csv, and log every operation to organizer.log.
# =============================================================================

SOURCE_FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

#  Check if the archive directory exists; create it if it doesn't
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir -p "$ARCHIVE_DIR"
    echo "   Archive directory created: '$ARCHIVE_DIR'"
else
    echo "  Archive directory '$ARCHIVE_DIR' already exists."
fi

#  Generate a timestamp string in YYYYMMDD-HHMMSS format
#  to make every archived filename unique so no file is overwritten.
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

#  Confirm the source file exists before attempting to archive it
if [ ! -f "$SOURCE_FILE" ]; then
    echo "[ERROR] '$SOURCE_FILE' not found in the current directory."
    echo "        Nothing to archive. Exiting."
    exit 1
fi

#  Build the new archived filename by inserting the timestamp 
BASENAME="${SOURCE_FILE%.csv}"                   
ARCHIVED_NAME="${BASENAME}_${TIMESTAMP}.csv"      # append timestamp - "grades_20251105-170000.csv"
ARCHIVED_PATH="${ARCHIVE_DIR}/${ARCHIVED_NAME}"   # full destination path

#  Move (rename + relocate) grades.csv into the archive folder 
mv "$SOURCE_FILE" "$ARCHIVED_PATH"

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to move '$SOURCE_FILE' to '$ARCHIVED_PATH'. Check permissions."
    exit 1
fi

echo "  Archived '$SOURCE_FILE'  →  '$ARCHIVED_PATH'"

# Workspace reset

echo "assignment,group,score,weight" > "$SOURCE_FILE"
echo " Fresh '$SOURCE_FILE' created and ready for the next batch."

# Add this operation’s details to the log file so each run keeps a record of when it happened, what was archived, and where it was saved.

{
    echo "------------------------------------------------------------"
    echo "Timestamp      : $TIMESTAMP"
    echo "Original file  : $SOURCE_FILE"
    echo "Archived as    : $ARCHIVED_PATH"
    echo "Logged at      : $(date '+%Y-%m-%d %H:%M:%S')"
    echo "------------------------------------------------------------"
} >> "$LOG_FILE"

echo "  Operation logged to '$LOG_FILE'."
echo ""
echo "Done. Workspace is reset and ready for the next batch of grades."
exit 0
