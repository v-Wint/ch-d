/**
 * Ad CSRF token to headers
 */
function tokenSetup() {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": (function()  {
                let c_name = "csrftoken";
                if (document.cookie.length > 0) {
                    let c_start = document.cookie.indexOf(c_name + "=");
                    if (c_start != -1) {
                        c_start = c_start + c_name.length + 1;
                        let c_end = document.cookie.indexOf(";", c_start);
                        if (c_end == -1) c_end = document.cookie.length;
                        return unescape(document.cookie.substring(c_start,c_end));
                    }
                }
                return "";
            })()
        }
    })
}

export { tokenSetup }
