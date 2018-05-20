
function createElement(value) {
    var el = document.createElement('li');
    var del = document.createElement('button');
    del.append('del')
    del.setAttribute('class', 'delete');
    del.setAttribute('data-record-id', value.id);
    el.append(del);
    el.append(' #' +value.id + ' [' + value.author_name + '] "' + value.message + '"');
    return el
}

function updateList() {
    var contentBlock = $('#record-items');
    contentBlock.html('');
    $.ajax('/api/records').done(function(data){
        data['records'].forEach(function (value) {
            contentBlock.append(createElement(value))
        });
        deleteHandle()
    })
}

function deleteHandle() {
    $('.delete').click(function () {
        var recId = $(this).data('recordId');
        $.ajax({
            'url': '/api/records/' + recId + '/',
            'type': 'DELETE'
        }).done(updateList)
    })
}

function addRecord() {
    var formDataArray = $('form').serializeArray(),
        formData = {};
    formDataArray.forEach(function (item) { formData[item.name] = item.value });
    $.ajax({
        'url': '/api/records/',
        'type': 'POST',
        'data':  JSON.stringify(formData),
        'contentType': 'application/json',
        'dataType': 'json',
    }).done(updateList)
}

$(document).ready(
    function () {
        updateList();
    }
);
