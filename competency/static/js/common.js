var CSRF_TOKEN = $("input[name='csrfmiddlewaretoken']").val();

var form2json = function(formid) {
  var data = $(formid).serializeArray();
  var returnJson = {};
  for (idx = 0; idx < data.length; idx++) {
    returnJson[data[idx].name] = data[idx].value
  }
  return returnJson;
}

var form2api = function(url,method,formid,donefunc,failfunc) {
  data = form2json(formid);
  data2api(url,method,data,donefunc,failfunc);
}

var data2api = function(url,method,data,donefunc,failfunc){
  $('.overlay').show();
  $.ajax({
    url : url,
    type : method,
    dataType : 'json',
    contentType: 'application/json',
    data: JSON.stringify(data),
    beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
                }
  }).done(function(data){
    CSRF_TOKEN = data.csrf_token;
    donefunc(data);
    $('.overlay').hide();
  }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
    failfunc(XMLHttpRequest, textStatus, errorThrown);
    $('.overlay').hide();
  });
}
var postfile2api = function(url,formid,donefunc,failfunc){
  $('.overlay').show();
  data = new FormData($(formid).get(0));
  token = $("input[name='csrfmiddlewaretoken']").val();
  $.ajax({
    url : url,
    type : "POST",
    processData: false,
    contentType: false,
    data: data,
    beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", token);
                }
  }).done(function(data){
    donefunc(data);
    $('.overlay').hide();
  }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
    failfunc(XMLHttpRequest, textStatus, errorThrown);
    $('.overlay').hide();
  });
}
$(function(){
  $('[data-toggle="tooltip"]').tooltip();
});