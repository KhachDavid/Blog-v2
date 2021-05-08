/**
 * @author David Khachatryan
 * @copyright Copyright 2021, Mat Ognutyun
 * @license GPL
 * @version 2.0.0
 * @host David Khachatryan
 * @email dkhachatryan@wisc.edu
 * @status production
 */

const asterisk = "<span class=\"asteriskField\">*</span>";

// Login page

// Username and Password translation
try {
    document.querySelector("[for='id_username']").innerHTML = "Օգտանուն" + asterisk;
} catch (error) {
    console.log(error);
}

try {
    document.querySelector("[for='id_password']").innerHTML = "Գաղտնաբառ" + asterisk;        
} catch (error) {
    console.log(error);
}

// Invalid credentials alert message translation
try {
    document.getElementsByClassName("m-0")[0].innerHTML = "<li>Սխալ ծածկանուն և/կամ գաղտնաբառ</li>";
} catch (error) {
    console.log(error);
}


// Register Page
try {
    document.getElementById("hint_id_username").innerHTML = 
                            "Պահանջներ։ 150 տառ կամ ավելի քիչ. Կարող է Պարունակել Տառեր, Թվեր և @/./+/-/_";
} catch (error) {
    console.log(error);
}

try {
    document.querySelector("[for='id_password1']").innerHTML = "Գաղտնաբառ" + asterisk;   
} catch (error) {
    console.log(error);
}

try {
    document.querySelector("[for='id_password2']").innerHTML = "Հաստատել Գաղտնաբառը" + asterisk;      
} catch (error) {
    console.log(error);
}

try {
    document.querySelector("[for='id_email']").innerHTML = "Էլ․ Հասցե" + asterisk;      
} catch (error) {
    console.log(error);
}

try {
    document.getElementById("hint_id_password1").innerHTML = 
                    "<ul><li>Ձեր Գաղտնաբառը Չի Կարող Նման Լինել Ձեր Անձնական Ինֆորմացիային</li><li>Ձեր Գաղտնաբառը Պետք է Ունենա Առնվազն 8 Տառ</li><li>Ձեր Գաղտնաբառը Չպետք է Լինի Հաճախ Օգտագործված (Օր․։ abc12345678)</li><li>Ձեր Գաղտնաբառը Չպետք է Պարունակի Միայն Թվեր</li></ul>";
} catch (error) {
    console.log(error);
}

try {
    document.getElementById("hint_id_password2").innerHTML =
                    "Մուտքագրեք Նույն Գաղտնաբառը Հաստատելու Համար";
} catch (error) {
    console.log(error);
}

try {
    var btn = document.getElementsByClassName("btn-outline-info");
    
    if (btn[0].innerHTML === "Գրանցվել") {
        btn[0].setAttribute("id", "pagination-buttons");
    }
} catch (error) {
    console.log(error);
}

try {
    document.getElementById("error_1_id_username").innerHTML =
                    "Այս օգտանունը զբաղված է";
} catch (error) {
    console.log(error);
}

try {
    document.getElementById("error_1_id_password2").innerHTML =
                    "Գաղտնաբառերը չեն համընկնում";
} catch (error) {
    console.log(error);
}