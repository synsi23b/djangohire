function form_toggle_nationality(event)
{
    let e = document.getElementById("id_nationality");
    let len = e.length;
    let sel = e.options[e.selectedIndex].value;
    console.log(sel);
    if(sel == "OTH")
    {
        e = document.getElementById("id_nation_other_col")
        e.style = "display: block;"
    }
    else
    {
        e = document.getElementById("id_nation_other_col")
        e.style = "display: none;"
    }
}

function form_attach_toggle_nationality()
{
    console.log("run attach nationality");
    let e = document.getElementById("id_nationality");
    e.addEventListener("change", form_toggle_nationality, false);
    console.log("run attach nationality fin");
    form_toggle_nationality(null);
}