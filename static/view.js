import { tokenSetup } from './setup.js';

import { transposeChordsForward, transposeChordsBackward, simplifyChords, setChordsClickListeners } from './chords.js';

(function () {
    let timeout;

    tokenSetup();

    /**
     * Save chord if not saved and remove from saved if saved
     */
    function saveEntry() {
        const button = $("#button-save");
        const url = button.attr('data-url');
        if (button.val() == 0) {
            $.ajax({
                url: url,
                type: 'POST',
                success: () => button.text('Remove chords').removeClass('btn-outline-light').addClass('btn-secondary').val(1)
            });
        } else {
            $.ajax({
                url:  url,
                type: 'DELETE',
                success: () => button.text('Save chords').addClass('btn-outline-light').removeClass('btn-secondary').val(0),
            });
        }
    }

    /**
     * Start scrolling the page
     */
    function scrollPage() {
        clearTimeout(timeout);
        window.scrollBy({
            "top": parseInt($('#scroll-count').text()),
            "behavior": "smooth"
        });

        if ($('#scroll-count').text()){
            timeout = setTimeout(scrollPage, 250);
        }
    }

    /**
     * Add comment on the page
     */
    function addComment() {
        const button = $("#button-comment");

        const input = $('#id_comment').val()
        $('#id_comment').val('')

        if (input){
            $.ajax({
                url: button.attr('data-url'),
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ 'body': input }),
                success: (response) => {
                    button.prop('disabled', false)
                    $(".comments").prepend(`
                    <div class="card my-3">
                        <div class="card-header">
                            <p class="float-start m-0">${response.user}</p>
                            
                            <p class="float-end m-0">${response.added_date}</p>
                        </div>
                        <div class="row m-0">
                            <div class="col-2 d-flex align-items-center justify-content-center p-0" >
                                <img class="card-img-top my-2 d-block w-75" src=${response.pfp ? "/media/" + response.pfp : "https://i.postimg.cc/jdSrCVyg/default.png"} alt="profile picture">
                            </div>
                            <div class="col-10 p-0">
                                <div class="card-body ">
                                    <div class="card-text">
                                        ${response.body}
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>`)
                }
            })
        }

    }

    /**
     * Add click listeners on the buttons and chords
     */
    (function addClickListeners() {
        $("#transpose-forward").on("click", transposeChordsForward);
        $("#transpose-backward").on("click", transposeChordsBackward);

        $("#simplify").on("click", simplifyChords);

        $('#button-save').click(saveEntry);

        
        $('#scroll-down').click(() => {
            $('#scroll-count').text(parseInt($('#scroll-count').text()) + 1);
            scrollPage();
        });
        $('#scroll-up').click(() => {
            let value = parseInt($('#scroll-count').text());
            $('#scroll-count').text(value > 0 ? value - 1 : 0);
        });
        $('#scroll-count').click(() => $('#scroll-count').text("0"));

        setChordsClickListeners();

        $("#button-comment").click(addComment);
        
        // on enter
        $("#id_comment").keypress((e) => {
            if (e.which == 13) {
                addComment();
            }
        })
    })()
})()
