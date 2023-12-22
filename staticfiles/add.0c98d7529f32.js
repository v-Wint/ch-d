(function () {
    /**
     * Set chords preview on process button click
     */
    (function setChordsPreview() {
        /**
         * Wrapp all the chords in text with span.chord tags
         * @param {string} text 
         * @returns Formated text
         */
        function processChordsText(text) {
            text = text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
            let result = "";
            for (let line of text.split("\n")) {
                // if 1 chord along a lot of words, it's not a chord
                if (line.split(/[\s]+/).length < 3 || (Array.from(line.matchAll(/([A-H](\#|b)?[augdimMaj7sus4b0-9\-\+]*)/g)) || []).length > 1) {
                    line = line.replaceAll(/([A-H](#|b)?[augdimMaj7sus4b0-9\-\+]*)(\s|$|\*|\]|\/)/g, (el) => {
                        if ('*]/'.includes(el[el.length-1])) {
                            let f = el[el.length-1];
                            return '\\' + el.slice(0, -1) + '\\' + f;
                        }
                        return '\\' + el.trim() + '\\' + el.match(/(\s|$)/)[0];
                    });
                }
                
                line = line.replaceAll(/\\+(?<group>[A-H](\#|b)?[augdimMaj7sus4b0-9\-\+]*)\\+/g, '<span class="chord">$<group></span>');
                result += line + "\n";
            }
            return result;
        }
        
        $('#process').click(() => $('#preview').html(processChordsText($('#id_text').val())));
    })();
    
    const BASE = window.location.href.split(':')[0] + '://' + window.location.href.split('/')[2] + '/api/';
    
    /**
     * Set autocomplete on author, song, tuning, capo and strumming fields
     */
    (function setAutocomplete() {
        $( "#id_author" ).autocomplete({
            source: BASE + "autocomplete/authors/"
        });
        
        $( "#id_song" ).autocomplete({
            source: BASE + "autocomplete/songs/"
        });
        $( "#id_tuning" ).autocomplete({
            source: BASE + "autocomplete/tunings/"
        });
        $( "#id_capo" ).autocomplete({
            source: BASE + "autocomplete/capos/"
        });
        $( "#id_strumming" ).autocomplete({
            source: BASE + "autocomplete/strummings/"
        });
    })();
    
    /**
     * Show warnings depending on api response
     */
    (function setWarnings() {
        $(".form-control").on("focusin focusout", () =>{
            $.ajax({url: BASE + "check/",
                data:{
                    author:$("#id_author").val(),
                    song:$("#id_song").val(),
                    tuning:$("#id_tuning").val(),
                    strumming:$("#id_strumming").val(),
                    capo:$("#id_capo").val()
                },
            }).done((data) => {
                $(".warnings").html(data.msg.split('\n').map((el) => `<p>${el}</p>`));
            })
        })  
    })();
})()
