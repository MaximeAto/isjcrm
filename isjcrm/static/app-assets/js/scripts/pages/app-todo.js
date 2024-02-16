/*=========================================================================================
    File Name: dashboard-ecommerce.js
    Description: dashboard-ecommerce
    ----------------------------------------------------------------------------------------
    Item Name: Modern Admin - Clean Bootstrap 4 Dashboard HTML Template
    Author: PIXINVENT
    Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/

// Todo App variables
var todoNewTasksidebar = $(".todo-new-task-sidebar"),
  appContentOverlay = $(".app-content-overlay"),
  sideBarLeft = $(".sidebar-left"),
  todoTaskListWrapper = $(".todo-task-list-wrapper"),
  todoItem = $(".todo-item"),
  selectAssignLable = $(".select2-assign-label"),
  selectUsersName = $(".select2-users-name"),
  avatarUserImage = $(".avatar-user-image"),
  updateTodo = $(".update-todo"),
  addTodo = $(".add-todo"),
  markCompleteBtn = $(".mark-complete-btn"),
  newTaskTitle = $(".new-task-title"),
  taskTitle = $(".task-title"),
  noResults = $(".no-results"),
  assignedAvatarContent = $(".assigned .avatar .avatar-content"),
  todoAppMenu = $(".todo-app-menu");

$(function () {
  "use strict";

  // if it is not touch device
  if (!$.app.menu.is_touch_device()) {
    // Sidebar scrollbar
    if ($('.todo-application .sidebar-menu-list').length > 0) {
      var sidebarMenuList = new PerfectScrollbar('.sidebar-menu-list', {
        theme: "dark",
        wheelPropagation: false
      });
    }

    //  New task scrollbar
    if (todoNewTasksidebar.length > 0) {
      var todo_new_task_sidebar = new PerfectScrollbar('.todo-new-task-sidebar', {
        theme: "dark",
        wheelPropagation: false
      });
    }

    // Task list scrollbar
    if ($('.todo-application .todo-task-list').length > 0) {
      var sidebar_todo = new PerfectScrollbar('.todo-task-list', {
        theme: "dark",
        wheelPropagation: false
      });
    }
  }
  // if it is a touch device
  else {
    $('.sidebar-menu-list').css("overflow", "scroll");
    $('.todo-new-task-sidebar').css("overflow", "scroll");
    $('.todo-task-list').css("overflow", "scroll");
  }

  // Single Date Picker
  $('.pickadate').daterangepicker({
    singleDatePicker: true,
    showDropdowns: true,
    locale: {
      format: 'YY/MM/DD'
    }
  });

  // dragable list
  dragula([document.getElementById("todo-task-list-drag")], {
    moves: function (el, container, handle) {
      return handle.classList.contains("handle");
    }
  });


  // select assigner
  selectUsersName.select2({
    placeholder: "Unassigned",
    dropdownAutoWidth: true,
    width: '100%'
  });

  // Sidebar scrollbar
  if ($('.todo-application .sidebar-menu-list').length > 0) {
    var sidebarMenuList = new PerfectScrollbar('.sidebar-menu-list', {
      theme: "rend",
      wheelPropagation: false
    });
  }

  //  New task scrollbar
  if (todoNewTasksidebar.length > 0) {
    var todo_new_task_sidebar = new PerfectScrollbar('.todo-new-task-sidebar', {
      theme: "dark",
      wheelPropagation: false
    });
  }

  // Task list scrollbar
  if ($('.todo-application .todo-task-list').length > 0) {
    var sidebar_todo = new PerfectScrollbar('.todo-task-list', {
      theme: "dark",
      wheelPropagation: false
    });
  }

  // New compose message compose field
  var composeEditor = new Quill('.snow-container .compose-editor', {
    modules: {
      toolbar: '.compose-quill-toolbar'
    },
    placeholder: 'Add Description..... ',
    theme: 'snow'
  });


  // **************Sidebar Left**************//
  // -----------------------------------------

  // Main menu toggle should hide app menu
  $('.menu-toggle').on('click', function () {
    sideBarLeft.removeClass('show');
    appContentOverlay.removeClass('show');
    todoNewTasksidebar.removeClass('show');
  });

  //on click of app overlay removeclass show from sidebar left and overlay
  appContentOverlay.on('click', function () {
    sideBarLeft.removeClass('show');
    appContentOverlay.removeClass('show');
  });

  // Add class active on click of sidebar menu's filters
  todoAppMenu.find(".list-group a").on('click', function () {
    var $this = $(this);
    todoAppMenu.find(".active").removeClass('active');
    $this.addClass("active")
  });

  //On compose btn click of compose mail visible and sidebar left hide
  $('.add-task-btn').on('click', function () {
    //show class add on new task sidebar,overlay
    todoNewTasksidebar.addClass('show');
    appContentOverlay.addClass('show');
    sideBarLeft.removeClass('show');
    // taskTitle.focus();
    //d-none add on avatar and remove from avatar-content
    avatarUserImage.addClass("d-none");
    assignedAvatarContent.removeClass("d-none");
    //select2 value null assign
    selectUsersName.val(null).trigger('change');
    selectAssignLable.val(null).trigger('change');
    //update button has add class d-none remove from add TODO
    updateTodo.addClass("d-none");
    addTodo.removeClass("d-none");
    //mark complete btn should hide & new task title will visible
    markCompleteBtn.addClass("d-none");
    newTaskTitle.removeClass("d-none");
    //Input field Value empty
    taskTitle.val("");
    var compose_editor = $(".compose-editor .ql-editor");
    compose_editor[0].innerHTML = "";
    selectAssignLable.attr("disabled", "true");
  });

  // On sidebar close click hide sidebarleft and overlay
  $(".todo-application .sidebar-close-icon").on('click', function () {
    sideBarLeft.removeClass('show');
    appContentOverlay.removeClass('show');
  });


  //**** fiter with left sidebar*****//

  // Fonction pour filtrer les éléments en fonction du statut
  function filterTasksByStatus(status) {
    // Masquer tous les éléments de la liste
    $('.todo-item').hide();
    
    // Afficher uniquement les éléments qui correspondent au statut sélectionné
    $('.todo-item[data-status="' + status + '"]').show();
  }

  // Gestionnaire de clic pour les filtres de la barre latérale
  $('.filter-item').on('click', function (event) {
    event.preventDefault();

    // Récupérer le statut associé au filtre
    var status = $(this).data('status');
    console.log(status);
    // Appliquer le filtre
    filterTasksByStatus(status);
  });

  // Gestionnaire de clic pour le filtre "All"
  $('#seeall.active').on('click', function (event) {
    event.preventDefault();

    // Afficher tous les éléments
    $('.todo-item').show();
  });



  // **************New Task sidebar**************//
  // ---------------------------------------------

  // add new task
  addTodo.on("click", function () {
    // check task assigned or not
    function renderAvatar(src) {
      if (src !== undefined) {
        return '<img src="' + src + '"alt="avatar" height="30" width="30" >'
      } else {
        return '<div class="avatar-content"><i class="ft-user font-medium-4"></i></div>'
      }
    };
    // if add task field are fiill and create a new task
    if (taskTitle.val().length > 0) {
      var titleTask = taskTitle.val(),
        selectAssign = $(".select2-users-name option:selected").val(),
        $randomID = Math.floor((Math.random() * 100) + Date.now()), //generate random id
        selectedVal = $(".select2-assign-label option:selected")

      var avatarSRC = todoTaskListWrapper.find("[data-name='" + selectAssign + "']").find(".avatar img").attr("src"); //Img src find if data name matches with list
      todoTaskListWrapper.append(
        // append a new task in task list
        '<li class="todo-item" data-name="' + selectAssign + '">' +
          '<div class="todo-title-wrapper d-flex justify-content-between align-items-center">' +
            '<div class="todo-title-area d-flex">' +
               '<i class="ft-more-vertical handle"></i>' +
                '<div class=" d-flex custom-control custom-checkbox">' +
                    '<input type="checkbox" class="custom-control-input" id="' + $randomID + '">' +
                    '<label class="custom-control-label" for="' + $randomID + '"></label>' + 
                '</div>' +
                '<p class="todo-title mx-50 m-0 truncate">' + titleTask + '</p>' +
            '</div>' + 
            '<div class="todo-item-action d-flex align-items-center">' +
              '<div class="avatar ml-1">' + renderAvatar(avatarSRC) + '</div>'+
              '<a class="todo-item-delete ml-75">' + '<i class="ft-trash-2"></i>' + '</a>' + 
            '</div>' + 
         '</div>'+
        '</li>');
      // new task sidebar, overlay hide
      todoNewTasksidebar.removeClass('show');
      appContentOverlay.removeClass('show');
      selectAssignLable.attr("disabled", "true");
    } else {
      // new task sidebar, overlay hide
      todoNewTasksidebar.removeClass('show');
      appContentOverlay.removeClass('show');
      selectAssignLable.attr("disabled", "true");
    }
  });

  // On Click of Close Icon btn, cancel btn and overlay remove show class from new task sidebar and overlay
  // and reset all form fields
  $(".close-icon, .cancel-btn, .app-content-overlay, .mark-complete-btn").on('click', function () {
    todoNewTasksidebar.removeClass('show');
    appContentOverlay.removeClass('show');
    setTimeout(function () {
      todoNewTasksidebar.find('textarea').val("");
      var compose_editor = $(".compose-editor .ql-editor");
      compose_editor[0].innerHTML = "";
      selectAssignLable.attr("disabled", "true");
    }, 100)
  });

  // Update Task
  updateTodo.on("click", function () {
    todoNewTasksidebar.removeClass('show');
    appContentOverlay.removeClass('show');
    selectAssignLable.attr("disabled", "true");
  });

  // ************Rightside content************//
  // -----------------------------------------

  // Search filter for task list
  $(document).on("keyup", ".todo-search", function () {
    todoItem = $(".todo-item");
    $('.todo-item').css('animation', 'none')
    var value = $(this).val().toLowerCase();
    if (value != "") {
      todoItem.filter(function () {
        $(this).toggle($(this).text().toLowerCase().includes(value));
      });
      var tbl_row = $(".todo-item:visible").length; //here tbl_test is table name

      //Check if table has row or not
      if (tbl_row == 0) {
        if (!noResults.hasClass('show')) {
          noResults.addClass('show');
        }
      } else {
        noResults.removeClass('show');
      }
    } else {
      // If filter box is empty
      todoItem.show();
      if (noResults.hasClass('show')) {
        noResults.removeClass('show');
      }
    }
  });
  // on Todo Item click show data in sidebar
  var globalThis = ""; // Global variable use in multiple function
  todoTaskListWrapper.on('click', '.todo-item', function (e) {
    var $this = $(this);
    globalThis = $this;

    var task_id = $this.attr('data-id');
    var task_deadline = $this.attr('data-deadline');
    var task_objective = $this.attr('data-objective');

    $('.pickadate').val(task_deadline)

    todoNewTasksidebar.addClass('show');
    appContentOverlay.addClass('show');

    var todoTitle = $this.find(".todo-title").text();
    taskTitle.val(todoTitle);
    var compose_editor = $(".compose-editor .ql-editor");
    compose_editor[0].innerHTML = task_objective;

    // if avatar is available
    if ($this.find(".avatar img").length) {
      avatarUserImage.removeClass("d-none");
      assignedAvatarContent.addClass("d-none");
    } else {
      avatarUserImage.addClass("d-none");
      assignedAvatarContent.removeClass("d-none");
    }
    //current task's image source assign to variable
    var avatarSrc = $this.find(".avatar img").attr('src');

    avatarUserImage.attr("src", avatarSrc);
    var assignName = $this.attr('data-name');

    $(".select2-users-name").val(assignName).trigger('change');

    // update button has remove class d-none & add class d-none in add todo button
    updateTodo.removeClass("d-none");
    addTodo.addClass("d-none");
    markCompleteBtn.removeClass("d-none");
    newTaskTitle.addClass("d-none");

  }).on('click', '.todo-item-favorite', function (e) {
    e.stopPropagation();
    $(this).toggleClass("warning");
    $(this).find("i").toggleClass("bxs-star");
  }).on('click', '.todo-item-delete', function (e) {
    e.stopPropagation();
    $(this).closest('.todo-item').remove();
  }).on('click', '.custom-checkbox', function (e) {
    e.stopPropagation();
  });

  // Complete task strike through
  todoTaskListWrapper.on('click', ".todo-item .custom-control-input", function (e) {
    $(this).closest('.todo-item').toggleClass("completed");
  });

  // Complete button click action
  markCompleteBtn.on("click", function () {
    globalThis.addClass("completed");
    globalThis.find(".custom-control-input").prop("checked", true);
    selectAssignLable.attr("disabled", "true");
  });

  // Todo sidebar toggle
  $('.sidebar-toggle').on('click', function (e) {
    e.stopPropagation();
    sideBarLeft.toggleClass('show');
    appContentOverlay.addClass('show');
  });

});

$(window).on("resize", function () {
  // remove show classes from sidebar and overlay if size is > 992
  if ($(window).width() > 992) {
    if (appContentOverlay.hasClass('show')) {
      sideBarLeft.removeClass('show');
      appContentOverlay.removeClass('show');
      todoNewTasksidebar.removeClass("show");
    }
  }
});
