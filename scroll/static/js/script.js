// start with first post
let counter = 1;

// load 20 posts at a time
const quantity = 50;


// when DOM loads, render the first 20 posts
document.addEventListener('DOMContentLoaded', load);

// at the end of the page while scrolling call the load()
window.onscroll = ()=>{
    if(window.innerHeight + window.scrollY >= document.body.offsetHeight){
        load();
    }
}
// load next set of 20 posts
function load(){
    const start = counter;
    const end = start + quantity - 1;

    // get new posts and add new posts
    fetch(`/scroll/posts?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data =>{
           data.posts.forEach(add_post);
    })
};

// add a new post with given contents to DOM
function add_post(contents){
     
    //create new post
    const post = document.createElement('div');
    post.className = 'post';
    post.innerHTML = contents;

    // add post to DOM
    document.querySelector('#posts').append(post);
}