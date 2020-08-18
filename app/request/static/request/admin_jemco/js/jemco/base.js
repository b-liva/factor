$(document).ready(function () {
    $('#autocomplete').autocomplete({
        serviceUrl: '/customer/autocomplete',
        contentType: 'application/json',
        dataType:'json',
        // lookup: arr,
        // onSearchComplete: function (query, suggestions) {
        //     alert(suggestions);
        // }
        // select: function (suggestion) {
        //     $(this).val(suggestion);
        //     console.log(suggestion);
        // }
        onSelect: function (suggestion) {
            // $(this).val(suggestion.data);
            document.cookie = "customer=" + '=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
            // document.cookie("customer", suggestion.data);
            document.cookie = "customer=" + suggestion.data;
            // alert('You selected: ' + suggestion.value + ', ' + suggestion.data);
        }
    });
    $('#cu_chosen').chosen();
});