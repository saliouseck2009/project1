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

        const div_username = document.createElement("div");
        div_username.setAttribute('class','h2 text-capitalize d-inline text-left');
        div_username.appendChild(document.createTextNode(data.user));
        divContent.appendChild(div_username);

        const div_rate = document.createElement("div");
        div_rate.setAttribute('class','d-inline text-center')
        div_rate.appendChild(document.createTextNode(`rate at ${data.rate}/5`));
        divContent.appendChild(div_rate);

        const div_text = document.createElement("div");
        div_text.appendChild(document.createTextNode(data.text));
        divContent.appendChild(div_text);

        const div_date = document.createElement("div");
        div_date.setAttribute('class','d-block text-right');
        div_date.appendChild(document.createTextNode(data.date));
        divContent.appendChild(div_date);



        
    }
});

// <div class="row ml-3 mr-3">
//                         <div class="h2 text-capitalize col">{{post.username}}</div>
//                         <div class="col text-center"> rated at {{post.rating_scale}}/5</div>
//                         <div class="col text-right" id="text_right">posted at {{post.created_at}}</div>
//                     </div>
//                     <div class="border ml-3 mb-3 mr-3 pl-3 pb-3 pr-3 pt-3">
//                         <div>it is a very interesting book</div>
//                     </div>

