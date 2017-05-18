(function () {
    function checkAndSubmit($ele, formPrefix, idSuffix) {
        var formID = $ele.attr('data-id');
        var inputID = '#id_' + formPrefix + '-' + formID + '-' + idSuffix;
        $(inputID).attr('checked', 'checked');
        $ele.closest('form').submit();
    }

    $('#basket_formset a[data-behaviours~="remove"]').click(function (event) {
        checkAndSubmit($(this), 'form', 'DELETE');
        event.preventDefault();
    });

})();