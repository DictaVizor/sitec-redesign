
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            };
        };
    };
    return cookieValue;
  }
  
var requestHeaders = {
    'Accept-Language': navigator.language,
    'X-CSRFToken': getCookie('csrftoken'),
  }

function suiSetRequestHeaders(xhr){
    xhr.setRequestHeader('Accept-Language', navigator.language)
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
    return xhr
}

Array.prototype.contains = function(v) {
  for (var i = 0; i < this.length; i++) {
    if (this[i] === v) return true;
  }
  return false;
};

Array.prototype.unique = function() {
  var arr = [];
  for (var i = 0; i < this.length; i++) {
    if (!arr.contains(this[i])) {
      arr.push(this[i]);
    }
  }
  return arr;
}


String.prototype.utf8_to_b64 = function() {
  return window.btoa(unescape(encodeURIComponent(this)));
}

String.prototype.b64_to_utf8 = function() {
  return decodeURIComponent(escape(window.atob(this)));
}

const { jsPDF } = window.jspdf;
