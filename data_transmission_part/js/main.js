var date = "";
function print_date_message()
{
    var e = document.getElementById("dates").value;
    document.getElementById( 
                    "message").innerHTML = "顯示日期 : " + e;  
    //window.alert(date_var);
    var date = "";
    if (e=="today")
    {
        date = "2021-12-28_example";
        
    }
    else
    {
        date = "2021-12-28_Pie chart of car accident";
        
    }     
    document.getElementById('imageBox').src = "picture/" + date + ".jpg";       
}

function initialize()
{
    document.getElementById( 
                    "message").innerHTML = "顯示日期 : 無";
    date = "";
    document.getElementById('imageBox').src = "";
}

window.onload = function()
{ 
    print_date_message();
    initialize();
    var name = "kk";
    var lengthOfName = name.length;
    //document.getElementById('message').innerHTML = name;  
  
};
