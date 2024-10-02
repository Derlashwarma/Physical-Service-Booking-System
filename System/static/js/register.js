$(document).ready(()=>{
    $("#next_btn").click((e)=>{
        $(".top_part").css('display','none');
        $(".bottom_part").css('display','flex');
        e.preventDefault()
    })
    $("#back_btn").click((e)=>{
        $(".bottom_part").css('display','none');
        $(".top_part").css('display','flex');
        e.preventDefault()
    })
    $("#id_is_worker_0").click(()=>{
        $(".to_find").text("Sign up to find talents")
    })
    $("#id_is_worker_1").click(()=>{
        $(".to_find").text("Sign up to find opportunities")
    })
})