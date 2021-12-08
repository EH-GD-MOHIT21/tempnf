function readyfunc() {
    clearInterval(id);
    var typed = new Typed("#typing1", {
        strings: ["NestedForms"],
        typeSpeed: 100,
        backSpeed: 60,
        loop: true
    });

    var typed = new Typed("#typing2", {
        strings: ["For Create Quizes.", "For Create Survays.", "For Create MCQ Exams.", "Just For Fun.", "By Mohit Satija."],
        typeSpeed: 100,
        backSpeed: 60,
        loop: true
    });

}

id = setInterval(readyfunc, 100);


// document.querySelector('.mainbody').style.display = 'none';