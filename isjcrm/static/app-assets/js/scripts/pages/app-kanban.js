/*=========================================================================================
    File Name: kanban.js
    Description: kanban plugin
    ----------------------------------------------------------------------------------------
    Item Name: Modern Admin - Clean Bootstrap 4 Dashboard HTML Template
    Author: PIXINVENT
    Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/

$(document).ready(function () {
  var kanban_curr_el, kanban_curr_item_id, kanban_item_title, kanban_data, kanban_item, kanban_users;


  // Kanban Board and Item Data passed by json
  var kanban_board_data = [{
    id: "kanban-board-1",
    title: "Marketing",
    item: [{
      id: "11",
      title: "Facebook Campaign 😎",
      border: "success",
      dueDate: "Feb 6",
      comment: 1,
      attachment: 3,
      users: [
        "../../../app-assets/images/portrait/small/avatar-s-11.png",
        "../../../app-assets/images/portrait/small/avatar-s-12.png"
      ]
    },
    {
      id: "12",
      title: "Type Something",
      border: "info",
      image: "../../../app-assets/images/banner/banner-21.jpg",
      dueDate: "Feb 10"
    },
    {
      id: "13",
      title: "Social Media Graphics",
      border: "warning",
      dueDate: "Jan 3",
      comment: 23,
      attachment: 4,
      users: [
        "../../../app-assets/images/portrait/small/avatar-s-1.png",
        "../../../app-assets/images/portrait/small/avatar-s-18.png"
      ]
    },
    {
      id: "14",
      title: "Book newspaper ads online in popular newspapers.",
      border: "danger",
      comment: 56,
      attachment: 2,
      users: [
        "../../../app-assets/images/portrait/small/avatar-s-26.png",
        "../../../app-assets/images/portrait/small/avatar-s-16.png"
      ]
    },
    {
      id: "15",
      title: "Twitter Marketing",
      border: "secondary"
    }
    ]
  },
  {
    id: "kanban-board-2",
    title: "UI Designing",
    item: [{
      id: "21",
      title: "Flat UI Kit Design",
      border: "secondary"
    },
    {
      id: "22",
      title: "Drag people onto a card to indicate that.",
      border: "info",
      dueDate: "Jan 1",
      comment: 8,
      users: [
        "../../../app-assets/images/portrait/small/avatar-s-24.png",
        "../../../app-assets/images/portrait/small/avatar-s-14.png"
      ]
    },
    {
      id: "23",
      title: "Application Design",
      border: "warning"
    },
    {
      id: "24",
      title: "BBQ Logo Design 😱",
      border: "primary",
      dueDate: "Jan 6",
      comment: 10,
      attachment: 6,
      badgeContent: "AK",
      badgeColor: "danger"
    }
    ]
  },
  {
    id: "kanban-board-3",
    title: "Developing",
    item: [{
      id: "31",
      title: "Database Management System (DBMS) is a collection of programs",
      border: "warning",
      dueDate: "Mar 1",
      comment: 10,
      users: [
        "../../../app-assets/images/portrait/small/avatar-s-20.png",
        "../../../app-assets/images/portrait/small/avatar-s-22.png",
        "../../../app-assets/images/portrait/small/avatar-s-13.png"
      ]
    },
    {
      id: "32",
      title: "Admin Dashboard 🙂",
      border: "success",
      dueDate: "Mar 6",
      comment: 7,
      badgeContent: "AD",
      badgeColor: "primary"
    },
    {
      id: "33",
      title: "Fix bootstrap progress bar with & issue",
      border: "primary",
      dueDate: "Mar 9",
      users: [
        "../../../app-assets/images/portrait/small/avatar-s-1.png",
        "../../../app-assets/images/portrait/small/avatar-s-2.png"
      ]
    }
    ]
  }
  ];

  // var candidates = document.currentScript.getAttribute('data-candidates')

  // console.log(candidates)
  // Kanban Board
  var KanbanExample = new jKanban({
    element: "#kanban-wrapper", // selector of the kanban container
    addItemButton: true, // add a button to board for easy item creation
    boards: kanban_board_data // data passed from defined variable
  });


  // Add html for Custom Data-attribute to Kanban item
  var board_item_id, board_item_el;
  // Kanban board loop
  for (kanban_data in kanban_board_data) {
    // Kanban board items loop
    for (kanban_item in kanban_board_data[kanban_data].item) {
      var board_item_details = kanban_board_data[kanban_data].item[kanban_item]; // set item details
      board_item_id = $(board_item_details).attr("id"); // set 'id' attribute of kanban-item

      (board_item_el = KanbanExample.findElement(board_item_id)), // find element of kanban-item by ID
        (board_item_users = board_item_dueDate = board_item_comment = board_item_attachment = board_item_image = board_item_badge =
          " ");

      // check if users are defined or not and loop it for getting value from user's array
      if (typeof $(board_item_el).attr("data-users") !== "undefined") {
        for (kanban_users in kanban_board_data[kanban_data].item[kanban_item].users) {
          board_item_users +=
            '<li class="avatar pull-up my-0">' +
            '<img class="media-object" src=" ' +
            kanban_board_data[kanban_data].item[kanban_item].users[kanban_users] +
            '" alt="Avatar" height="18" width="18">' +
            "</li>";
        }
      }
      // check if dueDate is defined or not
      if (typeof $(board_item_el).attr("data-dueDate") !== "undefined") {
        board_item_dueDate =
          '<div class="kanban-due-date mr-50">' +
          '<i class="ft-clock font-size-small mr-25"></i>' +
          '<span class="font-size-small">' +
          $(board_item_el).attr("data-dueDate") +
          "</span>" +
          "</div>";
      }
      // check if comment is defined or not
      if (typeof $(board_item_el).attr("data-comment") !== "undefined") {
        board_item_comment =
          '<div class="kanban-comment mr-50">' +
          '<i class="ft-message-square font-size-small mr-25"></i>' +
          '<span class="font-size-small">' +
          $(board_item_el).attr("data-comment") +
          "</span>" +
          "</div>";
      }
      // check if attachment is defined or not
      if (typeof $(board_item_el).attr("data-attachment") !== "undefined") {
        board_item_attachment =
          '<div class="kanban-attachment">' +
          '<i class="ft-link font-size-small mr-25"></i>' +
          '<span class="font-size-small">' +
          $(board_item_el).attr("data-attachment") +
          "</span>" +
          "</div>";
      }
      // check if Image is defined or not
      if (typeof $(board_item_el).attr("data-image") !== "undefined") {
        board_item_image =
          '<div class="kanban-image mb-1">' +
          '<img class="img-fluid" src=" ' +
          kanban_board_data[kanban_data].item[kanban_item].image +
          '" alt="kanban-image">';
        ("</div>");
      }
      // check if Badge is defined or not
      if (typeof $(board_item_el).attr("data-badgeContent") !== "undefined") {
        board_item_badge =
          '<div class="kanban-badge">' +
          '<div class="avatar bg-' +
          kanban_board_data[kanban_data].item[kanban_item].badgeColor +
          ' font-size-small font-weight-bold">' +
          kanban_board_data[kanban_data].item[kanban_item].badgeContent +
          "</div>";
        ("</div>");
      }
      // add custom 'kanban-footer'
      if (
        typeof (
          $(board_item_el).attr("data-dueDate") ||
          $(board_item_el).attr("data-comment") ||
          $(board_item_el).attr("data-users") ||
          $(board_item_el).attr("data-attachment")
        ) !== "undefined"
      ) {
        $(board_item_el).append(
          '<div class="kanban-footer d-flex justify-content-between mt-1">' +
          '<div class="kanban-footer-left d-flex">' +
          board_item_dueDate +
          board_item_comment +
          board_item_attachment +
          "</div>" +
          '<div class="kanban-footer-right">' +
          '<div class="kanban-users">' +
          board_item_badge +
          '<ul class="list-unstyled users-list cursor-pointer m-0 d-flex align-items-center">' +
          board_item_users +
          "</ul>" +
          "</div>" +
          "</div>" +
          "</div>"
        );
      }
      // add Image prepend to 'kanban-Item'
      if (typeof $(board_item_el).attr("data-image") !== "undefined") {
        $(board_item_el).prepend(board_item_image);
      }
    }
  }


  // kanban Item - Pick-a-Date
  $(".edit-kanban-item-date").pickadate();

  // Perfect Scrollbar - card-content on kanban-sidebar
  if ($(".kanban-sidebar .edit-kanban-item .card-content").length > 0) {
    var kanbanSidebar = new PerfectScrollbar(".kanban-sidebar .edit-kanban-item .card-content", {
      wheelPropagation: false
    });
  }

});
