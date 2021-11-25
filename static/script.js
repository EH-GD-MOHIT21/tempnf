var main_div = document.getElementById('outer');
var add_more_mcq = document.getElementById('mcq-adder');
var add_more_ftp = document.getElementById('ftp-adder');


add_more_mcq.onclick = function() {
    var div = document.createElement('div');
    div.setAttribute('class', 'question-prototype');

    // qus
    var qus = document.createElement('textarea');
    qus.setAttribute('name', 'questionmcq');
    qus.setAttribute('class', 'question-box');
    qus.setAttribute('placeholder', 'Enter Your Question Here');
    qus.required = true;
    div.appendChild(qus);

    // options
    var opts = ['A', 'B', 'C', 'D']
    for (var i = 0; i < 4; i++) {
        var cdiv = document.createElement('div');
        cdiv.setAttribute('class', 'main-icoinput');

        // icon
        var ico = document.createElement('i');
        ico.setAttribute('class', 'far fa-circle');
        cdiv.appendChild(ico);

        var inp = document.createElement('input');
        inp.setAttribute('type', 'text');
        inp.setAttribute('class', 'option-box');
        inp.setAttribute('name', 'option' + (i + 1));
        inp.setAttribute('placeholder', 'option ' + opts[i]);

        cdiv.appendChild(inp);
        div.appendChild(cdiv);
    }

    // <div class="ismulticorrect">
    // <input type="hidden" name="multicorrect" id="mc0">
    // <input type="checkbox" onchange="mfsetcheck('mc0',this)">
    // </div>

    var pdiv = document.createElement('div');
    pdiv.setAttribute('class', 'ismulticorrect');

    var pinp = document.createElement('input');
    pinp.setAttribute('type', 'hidden');
    pinp.setAttribute('name', 'multicorrect');
    pdiv.appendChild(pinp);

    var cinp = document.createElement('input');
    cinp.setAttribute('type', 'checkbox');
    cinp.onchange = function() {
        if (this.checked) {
            pinp.value = 1;
        } else {
            pinp.value = 0;
        }
    }

    pdiv.appendChild(cinp);
    var spn = document.createElement('span');
    spn.textContent = " More than one choice";
    pdiv.appendChild(spn);
    div.appendChild(pdiv);

    var delbtn = document.createElement('button');
    delbtn.setAttribute('type', 'button');
    delbtn.setAttribute('class', 'delbtn');
    delbtn.textContent = "Delete";
    delbtn.onclick = function() {
        this.parentElement.remove();
    }
    div.appendChild(delbtn);
    main_div.appendChild(div);
    myspecialshitquery();
}

add_more_ftp.onclick = function() {
    var div = document.createElement('div');
    div.setAttribute('class', 'question-prototype');

    var textarea = document.createElement('textarea');
    textarea.setAttribute('name', 'questionftp');
    textarea.setAttribute('class', 'question-box');
    textarea.setAttribute('placeholder', 'Enter Your Question Here');
    textarea.required = true;

    var delbtn = document.createElement('button');
    delbtn.setAttribute('type', 'button');
    delbtn.setAttribute('class', 'delbtn');
    delbtn.textContent = "Delete";
    delbtn.onclick = function() {
        this.parentElement.remove();
    }
    div.appendChild(textarea);
    div.appendChild(delbtn);
    main_div.appendChild(div);
    myspecialshitquery();
}


// Auto scailing text-areas


$('#Form-title').on('input', function() {
    this.style.height = 'auto';

    this.style.height =
        (this.scrollHeight) + 'px';
});


$('#Form-Desc').on('input', function() {
    this.style.height = 'auto';

    this.style.height =
        (this.scrollHeight) + 'px';
});


function myspecialshitquery() {
    $('textarea').on('input', function() {
        this.style.height = 'auto';

        this.style.height =
            (this.scrollHeight) + 'px';
    });
}

function mfsetcheck(id, checkelm) {
    if (checkelm.checked) {
        document.getElementById(id).value = 1;
    } else {
        document.getElementById(id).value = 0;
    }
}

myspecialshitquery();