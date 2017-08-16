function convert_date_to_db(date) {
    var date_split = date.split('.');
    var day = date_split[0];
    var month = date_split[1];
    var year = date_split[2];
    return year + '-' + month + '-' + day
}

