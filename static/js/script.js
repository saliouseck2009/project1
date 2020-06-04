document.addEventListener('DOMContentLoaded', () => {
    // const template = Handlebars.compile(document.querySelector('#create-post').innerHTML);                 
    const formData = new FormData()
    /*let review = document.querySelector(".review").innerHTML;*/
    
    document.querySelectorAll('#button_note').forEach( (button) => {
        button.onclick=()=>{
            document.querySelectorAll('#button_note').forEach((b)=>{
                button.style.backgroundColor="#F0F8FF";
                button.style.color="#007bff";
                button.style.borderColor="#007bff";
                button.style.border="1px solid transparent";
            });
            button.style.backgroundColor="#007bff";
            button.style.color="white";
            const note = button.dataset.rate;
            formData.append('rate',note);
            console.log(formData);
        };
    });

    document.onsubmit= ()=>{
        const text = document.querySelector('.text').value;
        formData.append('text', text);
        // formData.append('id_book', id_book);
        console.log(formData);
        load();
        return false;
    };
    function load() {
        const request = new XMLHttpRequest();
        request.open('POST', '/review');
        console.log(formData);
        request.send(formData);
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            console.log("loaded");
            if (data.error){
                const span = document.createElement('span');
                span.appendChild(document.createTextNode(data.error));
                span.style.color ="red";
                document.querySelector('.duplicate').appendChild(span);
            }else{
                createComment(data);
                // console.log(data.user);
                // const newPost = template({'date': data.date, 'user': data.user, 'text': data.text});
                // document.querySelector(".review").innerHTML += newPost;
                /*review =  newPost + review;*/
            } 
        };   
    }; 
    
    function createComment(data){
        const divContent = document.createElement("div");
        divContent.setAttribute('class', 'stats');
        const review = document.querySelector('.review');
        review.appendChild(divContent);

        const span_username = document.createElement("span");
        span_username.setAttribute('class','h2 text-capitalize');
        span_username.appendChild(document.createTextNode(data.user));
        divContent.appendChild(span_username);

        const span_rate = document.createElement("span");
        span_rate.appendChild(document.createTextNode(`rate at ${data.rate}/5`));
        divContent.appendChild(span_rate);

        const span_date = document.createElement("span");
        span_date.setAttribute('id','text_right');
        span_date.appendChild(document.createTextNode(data.date));
        divContent.appendChild(span_date);

        const div_text = document.createElement("div");
        div_text.setAttribute('class','lead');
        div_text.appendChild(document.createTextNode(data.text));
        divContent.appendChild(div_text);


        
    }
});
            
