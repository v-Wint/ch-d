const CYCLE_FORWARD = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A'];
const CHORDS_MAP_FORWARD = {"Db":"C#", "Eb":"D#", "Gb":"F#", "Ab":"G#", "Bb":"A#", "H": "B", "Hb": "A#", };
const CYCLE_BACKWARD = ['A', 'Ab', 'G', 'Gb', 'F', 'E', 'Eb', 'D', 'Db', 'C', 'B', 'Bb', 'A'];
const CHORDS_MAP_BACKWARD = {"C#": "Db", "D#": "Eb", "F#": "Gb", "G#": "Ab", "A#": "Bb", "H": "B", "Hb": "Bb"};

/**
 * Transpose a chord 1 key forward
 * @param {string} chord 
 * @returns Replaced chord
 */
function transposeChordForward(chord) {
    return chord.replace(/[A-H](b|#)?/g, (match) => {
        return CYCLE_FORWARD[CYCLE_FORWARD.indexOf(CHORDS_MAP_FORWARD[match] || match) + 1];
    })
}

/**
 * Transpose a chord 1 key backward
 * @param {string} chord 
 * @returns {string} Replaced chord
 */
function transposeChordBackward(chord) {
    return chord.replace(/[A-H](b|#)?/g, (match) => {
        return CYCLE_BACKWARD[CYCLE_BACKWARD.indexOf(CHORDS_MAP_BACKWARD[match] || match) + 1];
    });   
    
}

/**
 * Replace a chord with a chord consisting only of the base, e.g. Am7sus2 becomes Am
 * @param {string} chord 
 * @returns {string} Simplified chord
 */
function simplifyChord(chord) {
    return chord.replace(/>(.*?)</, (match) => {
        return '>' + match.match(/[A-H](b|#)?[m]?/g) + '<';
    })
}

/**
 * Apply the rule to all the chords in text div
 * @param {function} rule function which replaces a chord with a new value
 */
function changeAllChords(rule) {
    let text = $(".text").first().html();

    text = text.replaceAll(/ *<span class="chord">(.*?)<\/span> */g, (match) => {
        let init = match;
        match = rule(match);
        
        // if chord grew, delete spaces after
        if (init.length < match.length && init.match(/ *$/)[0].length > 2 ) {
            return match.slice(0, -2);
        }
        // if chord length shrank, add spaces after
        if (init.length > match.length && init.match(/ *$/)[0].length > 2 ) {
            return match + ' '.repeat(2 * (init.length - match.length));
        }
        return match;
    });

    $(".text").first().html(text);
    // set click listeners again
    setChordsClickListeners();
    // clear popups
    $(`.card-chord`).each((i, el) =>  $(el).remove());
}

/**
 * Transpose all the chords in text div 1 key forward
 */
function transposeChordsForward() {
    changeAllChords(transposeChordForward);
    $("#transpose-counter").text(parseInt($("#transpose-counter").text()) + 1);

}
/**
 * Transpose all the chords in text div 1 key backward
 */
function transposeChordsBackward() {
    changeAllChords(transposeChordBackward);
    $("#transpose-counter").text(parseInt($("#transpose-counter").text()) - 1);

}

/**
 * Simplify all the chords in text div
 */
function simplifyChords() {
    changeAllChords(simplifyChord);
}


const BASES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const BLACKS = [1, 3, 25, 6, 8, 10, 25, 13, 15, 25, 18, 20, 22]; // 25 if at that place we don't have black key

/**
 * Convert chord to a sequence of keys
 * @param {string} chord  
 * @returns {Array} Array of keys in the chords, starting with C, black keys included
 */
function toPianoSequence(chord) {
    let [, base, m, rem, ...rest] = chord.match(/([A-H\#b]+)(m|maj|Maj)?([augddimaj7sus4b0-9\-\+]*)/);
    
    // get the key number of base key
    let b = BASES.indexOf(CHORDS_MAP_FORWARD[base] || base);

    rem = rem || '';
    // some logic
    if (rem.includes('sus2')) {
        return rem.includes('7') ? [b, b+2, b+7, b+10] : [b, b+5, b+7];
    }

    if (rem.includes('sus')) {
        return rem.includes('7') ? [b, b+5, b+7, b+10] : [b, b+5, b+7];
    }

    if (rem.includes('7-5' || rem.includes('7#5')) ) {
        return m ? [b, b+3, b+6, b+10] : [b, b+4, b+6, b+10];
    }

    if (rem.includes('7+')) {
        return [b, b+4, b+8, b+10];
    }

    if (rem.includes('5')) {
        return [b, b+7];
    }

    if (rem.includes('6')) {
        return m ? [b, b+3, b+7, b+9] : [b, b+4, b+7, b+9];
    }

    if (rem.includes('maj7')) {
        return [b, b+3, b+7, b+11];
    }

    if (rem.includes('7')) {
        return m ? [b, b+3, b+7, b+10] : [b, b+4, b+7, b+10];
    }

    if (rem.includes('aug' || rem.includes('+'))) {
        return [b, b+4, b+8];
    }

    if (rem.includes('dim7')) {
        return [b, b+3, b+6, b+10];
    }

    if (rem.includes('dim')) {
        return [b, b+3, b+7];
    }

    if (rem.includes('add2') || rem.includes('add9')) {
        return m ? [b, b+2, b+3, b+7] : [b, b+2, b+4, b+7];
    } 

    return m ? [b, b+3, b+7] : [b, b+4, b+7];
}

/**
 * Convert a chord to a chord suitable for Raphael Chord library
 * @param {string} chord 
 * @returns {string} Chord formatted like A min7
 */
function toRaphelChord(chord) {
    let [, base, m, rem, ...rest] = chord.match(/([A-H\#b]+)(m|maj|Maj)?([augdimaj7sus4b0-9\-\+]*)/);
    m = m == 'm' ? 'min' : 'maj';
    rem = rem || '';

    if (Raphael.chord.find(base, m + rem)) {
        return base + ' ' + m + rem
    } else {
        return toRaphelChord(chord.match(/[A-H](b|#)?[m]?/g)[0])
    }
    
}

const pianoSVG = `<svg version="1.0" xmlns="http://www.w3.org/2000/svg"
width="128.000000pt" height="64.000000pt" viewBox="0 0 128.000000 64.000000"
preserveAspectRatio="xMidYMid meet">
<g transform="translate(0.000000,64.000000) scale(0.0100000,-0.0100000)"
fill="#000000" stroke="none">
<path d="M0 3205 l0 -1995 6400 0 6400 0 0 1995 0 1995 -6400 0 -6400 0 0
-1995z m690 840 l0 -1135 110 0 110 0 0 -840 0 -840 -445 0 -445 0 0 1975 0
1975 335 0 335 0 0 -1135z m910 0 l0 -1135 115 0 115 0 0 -840 0 -840 -450 0
-450 0 0 840 0 840 115 0 115 0 0 1135 0 1135 220 0 220 0 0 -1135z m1140
-840 l0 -1975 -445 0 -445 0 0 840 0 840 110 0 110 0 0 1135 0 1135 335 0 335
0 0 -1975z m680 845 l0 -1130 115 0 115 0 0 -845 0 -845 -445 0 -445 0 0 1975
0 1975 330 0 330 0 0 -1130z m910 -5 l0 -1135 110 0 110 0 0 -840 0 -840 -440
0 -440 0 0 845 0 845 110 0 110 0 0 1130 0 1130 220 0 220 0 0 -1135z m920 0
l0 -1135 115 0 115 0 0 -840 0 -840 -450 0 -450 0 0 830 c0 457 0 833 0 838 0
4 49 8 110 10 l110 3 0 1134 0 1135 225 0 225 0 0 -1135z m1130 -840 l0 -1975
-440 0 -440 0 0 840 0 840 110 0 110 0 0 1135 0 1135 330 0 330 0 0 -1975z
m702 883 c-2 -601 0 -1112 3 -1135 l6 -43 105 0 104 0 0 -840 0 -840 -440 0
-440 0 0 1975 0 1975 333 0 332 0 -3 -1092z m918 -40 l0 -1133 112 -3 113 -3
-3 -839 -2 -840 -450 0 -450 0 0 840 0 839 118 3 117 3 3 1133 2 1132 220 0
220 0 0 -1132z m1130 -843 l0 -1975 -440 0 -440 0 -2 840 -3 839 110 3 110 3
3 1133 2 1132 330 0 330 0 0 -1975z m692 843 l3 -1133 108 -5 107 -5 0 -835 0
-835 -445 -3 -445 -2 0 1975 0 1975 335 0 335 0 2 -1132z m898 -3 l0 -1135
115 0 115 0 0 -840 0 -840 -440 0 -440 0 0 840 0 840 110 0 110 0 0 1135 0
1135 215 0 215 0 0 -1135z m925 3 l0 -1133 118 -3 117 -3 0 -839 0 -840 -455
0 -455 0 0 840 0 840 110 0 110 0 0 1135 0 1135 228 0 227 0 0 -1132z m1135
-843 l0 -1975 -440 0 -440 0 0 840 0 839 108 3 107 3 3 1133 2 1132 330 0 330
0 0 -1975z"/>
</g>
</svg>`

/**
 * Set click listeners on all the chords to show applicatures popups
 */
function setChordsClickListeners() {
    let zindex = 1;

    function main() {
        $(".chord").each((i, el) => {

            // set click event listeners
            $(el).click(function() {
                zindex++;
                // if popup exists, remove
                if ($(`#chord${i}`).length) {
                    $(`#chord${i}`).remove();
                    return;
                }
                // create card underneath chord with id
                let pos = $(el).position();
                $(el).after(`<div class="card card-chord bg-secondary bg-gradient" id="chord${i}" style="position: absolute; top: ${pos['top']+30}px; left: ${pos['left']-40}px;z-index:${zindex};" ></div>`);
                
                // remove card on click
                $(`#chord${i}`).click(() => {$(`#chord${i}`).remove()});

                // if piano 
                if ($("#instrument option:selected").val() == 1) {
                    $(`#chord${i}`).append(pianoSVG);
                    for (const index of toPianoSequence($(el).text())) {
                        // if key is black
                        if (BLACKS.includes(index)) {
                            // go the number of spaces equal to the position in black keys list
                            $(`#chord${i} svg`).append(`<circle cx="${9.1 + (BLACKS.indexOf(index)) * 9.15}" cy="28" r="3" fill="#FFF" stroke="#FFF"></circle>`)
                        } else {
                            // go the number of spaces equal to index minus number of black keys before this key
                            $(`#chord${i} svg`).append(`<circle cx="${4.65 + (index - BLACKS.filter(number => number < index).length) * 9.13 }" cy="45" r="3" fill="#000000" stroke="#000"></circle>`)
                        }
                    }
                    $(`#chord${i}`).html($(`#chord${i}`).html());
                    return;
                }
                // if guitar
                Raphael.chord(`chord${i}`, toRaphelChord($(el).text()));
                $(`#chord${i} tspan`).attr('dy', '3.5px');
            })
        })
    }
    main();
}

export { transposeChordsForward, transposeChordsBackward, simplifyChords, setChordsClickListeners }
