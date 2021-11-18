var main_div = document.getElementById('outer');
var add_more_mcq = document.getElementById('content-adderbutton');
var add_more_fill = document.getElementById('content-adderbuttonftp');
starter_ftp = 1
used = []

add_more_mcq.onclick = function() {
    // div and its properties
    var div = document.createElement('div');
    div.setAttribute('class', 'question-prototype');
    // textarea created
    var new_field = document.createElement('textarea');
    new_field.setAttribute("name", "questionmcq")
    new_field.setAttribute("class", "question-box")
    new_field.setAttribute("placeholder", "Enter Your Question Here")
        // added textarea to div
    div.appendChild(new_field)

    temp_used = []
    var choices = ['A', 'B', 'C', 'D']
    for (var i = 1; i <= 4; i++) {
        while (true) {
            time = Math.floor(Math.random() * 100000000);
            if (used.indexOf(time) == -1) {
                break
            }
        }
        used.push(time)
        temp_used.push(time)
        console.log(used)
        var cd1 = document.createElement('div')
        cd1.setAttribute("class", "main-icoinput")
        var hiddeninp1 = document.createElement('input')
        hiddeninp1.setAttribute('type', 'hidden')
        hiddeninp1.setAttribute('name', 'radio' + i)
        hiddeninp1.setAttribute('value', 0)
        hiddeninp1.setAttribute('id', time + "f")

        var inp1 = document.createElement('input')
        inp1.setAttribute('type', 'checkbox')
        inp1.setAttribute('id', time)

        cd1.appendChild(hiddeninp1)
        cd1.appendChild(inp1)
        var inp11 = document.createElement('input')
        inp11.setAttribute('type', 'text')
        inp11.setAttribute('class', 'option-box')
        inp11.setAttribute('name', 'option' + i)
        inp11.setAttribute('placeholder', 'option ' + choices[i - 1])
        cd1.appendChild(inp11)
        div.appendChild(cd1)
    }

    var child = document.createElement('div');
    child.setAttribute("class", "main-icoinput");
    child.setAttribute("style", "text-align:right;")

    var childinp = document.createElement('input');
    childinp.setAttribute("type", "number")
    childinp.setAttribute("class", "option-box")
    childinp.setAttribute("name", "markmcq")
    childinp.setAttribute("placeholder", "enter question marks")
    childinp.setAttribute("value", 1)

    child.textContent = "Marks: "

    child.appendChild(childinp)
    div.appendChild(child)

    childinp.oninput = function() {
        if (document.getElementById("impmohit1").value == '') {
            document.getElementById(id).value = 0;
            alert("Question marks either positive or zero it'll be terminated in backend.")
        }
        if (parseInt(this.value) < 0) {
            this.value = 0;
            alert("Question marks either positive or zero it'll be terminated in backend.")
        }
        if (parseInt(this.value) > 1000) {
            this.value = 1000;
            alert("Question marks can be maximum 1000.")
        }
    }

    var button = document.createElement('button');
    button.setAttribute("type", "button");
    button.setAttribute("class", "delbtn");
    button.textContent = "delete";
    button.onclick = function() {
        this.parentElement.remove();
    }
    div.appendChild(button)
    main_div.appendChild(div)
    myspecialshitquery();
    // id = setInterval(() => {
    movequery(temp_used);
    // }, 100);
}

add_more_fill.onclick = function() {
    var div = document.createElement('div');
    div.setAttribute('class', 'question-prototype');
    var new_field = document.createElement('textarea');
    new_field.setAttribute("name", "ftp");
    new_field.setAttribute("id", starter_ftp);
    starter_ftp += 1;
    new_field.setAttribute("class", "question-box");
    new_field.setAttribute("placeholder", "Enter Your Question Here(Written ans type)");
    new_field.setAttribute("required", true);

    div.appendChild(new_field);


    var child = document.createElement('div');
    child.setAttribute("class", "main-icoinput");
    child.setAttribute("style", "text-align:right;")

    var childinp = document.createElement('input');
    childinp.setAttribute("type", "number")
    childinp.setAttribute("class", "option-box")
    childinp.setAttribute("name", "markfilltype")
    childinp.setAttribute("placeholder", "enter question marks")
    childinp.setAttribute("value", 1)

    child.textContent = "Marks: "

    child.appendChild(childinp)
    div.appendChild(child)

    var button = document.createElement('button');
    button.setAttribute("type", "button");
    button.setAttribute("class", "delbtn");
    button.textContent = "delete";
    button.onclick = function() {
        this.parentElement.remove()
    }
    div.appendChild(button);
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


function mohit(id) {
    console.log(id);
    if (parseInt(document.getElementById(id + "f").value) == 0) {
        (document.getElementById(id + "f").value = 1)
    } else {
        (document.getElementById(id + "f").value = 0)
    }
    console.log(document.getElementById(id + "f").value)
}

function movequery(temp_used) {
    for (var i = 0; i < temp_used.length; i++) {
        document.getElementById(temp_used[i]).addEventListener("change", function() {
            mohit(this.id);
        })
    }
}

myspecialshitquery();

function remove(arr, elm) {
    temp_arr = []
    for (var i = 0; i < arr.length; i++) {
        if (arr[i] != elm)
            temp_arr.push(arr[i])
    }
    return temp_arr
}