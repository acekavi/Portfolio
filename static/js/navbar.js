// $(document).ready(function () {
//   $("#navbarSideCollapse").click(function () {
//     $(".offcanvas-collapse").toggleClass("open")
//   });

//   $("#comment-form div").addClass("form-floating mb-3");
//   $("#comment-form div").each((index, element)=>{
//     $(element).children("input, textarea").eq(0).insertBefore($(element).children("label").eq(0))
//   })
// })

$(document).ready(function () {
  $(".IconContainer").click(function () {
    $(".IconContainer").toggleClass("change");
    $(".navLinks").toggle("slow");
  });
});