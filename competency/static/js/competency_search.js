var LAST_WORDS = "";
var PAGEINFO = {};
var PAGE_LOADING = 0;
var ALL_TASKS = {};
var ALL_ITEMS = {};

var search = function(query) {
    if( LAST_WORDS != "" && query == LAST_WORDS ){
        return;
    }
    if( query != "" ){
      const address = new URL(window.location);
      address.searchParams.set('q', query);
      history.replaceState("", "", address.toString());
    }
    $('#search-results').empty();
    ALL_TASKS = {};
    LAST_WORDS = query;
    get_page(1);
}

var get_page = function(page) {
    url = $('#word-search-form').attr('api-url');
    $.ajax({
        url : url,
        type : "GET",
        dataType : 'json',
        data : {
            q : LAST_WORDS,
            perpage : 18,
            page : page
        }
    }).done(function(data){
        if('OK' != data['result']){
            alert('error');
            return;
        }
        PAGEINFO = data.pageinfo;
        $('#total-count').text(data.pageinfo.count);
        for(let num=0; num < data.data.length; ++num){
            ALL_TASKS[data.data[num].code] = data.data[num];
            var card = $('#template-card').clone();
            idstr = 'card-' + data.data[num].id;
            taskcode = data.data[num].code;
            card.attr('id',idstr);
            card.appendTo('#search-results');
            card.show();
            parent = data.data[num].parent;
            root = data.data[num].parent.parent;
            $('#'+idstr+' .task-tree').text(root.name + ' -> ' + parent.name);
            $('#'+idstr+' .card-title').text(data.data[num].name);
            for(let i=0; i<data.data[num].items.length; ++i){
                item = data.data[num].items[i];
                ALL_ITEMS[item.code] = item;
                str = item.name.replace(LAST_WORDS,"<span class='text-danger'>"+LAST_WORDS+"</span>");
                tr = "<tr><td class='small'>" + str
                    + "</td><td class='small'><button class='btn btn-primary btn-sm text-nowrap btn-item-select' data-id='"
                    + item.code + "' id='select-btn-" + item.id + "' task-code='" + taskcode + "'>選択</button></td></tr>";
                li = '<li class="nav-item"><a href="#" class="nav-link">'+str+' <span class="float-right badge bg-primary">追加</span></a></li>';
                $('#'+idstr+' .task-items').append(tr);
                $('#'+idstr+' .task-evaluation-items').append(li);
                add_select_action('#select-btn-'+item.id);
            }
            for(let i=0; i<data.data[num].profiles.length; ++i){
                profile = data.data[num].profiles[i];
                badge = '<span class="badge badge-secondary">'+profile.name+'</span> '
                $('#'+idstr+' .card-footer').append(badge);
            }
        }
    }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
        alert(textStatus);
    });
}

var add_select_action = function(id){
    $(id).on('click',function(e){
        itemCode = $(this).attr('data-id');
        item = ALL_ITEMS[itemCode];
        add_evaluation_item(itemCode,item,'#target-items','.added-number');
        $('.control-sidebar').addClass('active');
        var get_class = $("body").attr('class');
        if (get_class == "fixed layout-top-nav control-sidebar-slide-open") {
            //$('body').removeClass('control-sidebar-open');
        } else {
            $('#open-csidebar').click();
        }
    });
}

var get_selected_items = function(){
    selected_items = JSON.parse(localStorage.getItem('SELECTED_ITEMS'));
    if(selected_items){
        return selected_items;
    }else{
        return {}
    }
}

var add_evaluation_item = function(itemCode,item, listAreaSelector, itemCountSelector){
    selected_items = get_selected_items();
    if(selected_items){
        selected_items[itemCode] = item;
    } else {
        selected_items = {}
        selected_items[itemCode] = item;
    }
    console.log(selected_items);
    localStorage.setItem('SELECTED_ITEMS', JSON.stringify(selected_items));
    show_selected_items(listAreaSelector, itemCountSelector);
}

var remove_evaluation_item = function(itemCode, listAreaSelector, itemCountSelector){
    selected_items = get_selected_items();
    if(selected_items){
        delete selected_items[itemCode];
        localStorage.setItem('SELECTED_ITEMS', JSON.stringify(selected_items));
        show_selected_items(listAreaSelector, itemCountSelector);
    }
}

var show_selected_items = function(listAreaSelector, itemCountSelector){
    selected_items = get_selected_items();
    $(listAreaSelector).empty();
    for( itemCode in selected_items ) {
        item = selected_items[itemCode];
        task = item.task_evaluation;
        row = '<div class="card card-outline card-primary">'
        + '<div class="card-header small"><div class="card-title"><span class="small">'
            + task.name
            + '</span></div><div class="card-tools">'
                +'<button type="button" class="btn btn-tool" data-card-widget="remove" id="item-remove-'+item.id
                +'" item-code="'+itemCode
                +'" task-code="'+task.code
                +'"><i class="fas fa-times"></i></button></div>'
        + '</div>'
        + '<div class="card-body small p-2">'
            + item.name
        + "</div>"
        + "</div>";
        $(listAreaSelector).append(row);
        $('#item-remove-'+item.id).on('click',function(e){
            itemCode = $(this).attr('item-code');
            taskCode = $(this).attr('task-code');
            remove_evaluation_item(itemCode, listAreaSelector, itemCountSelector);
        });
        $(itemCountSelector).text(Object.keys(selected_items).length);
    }
  }

  var create_target = function(formSelector){
    data = form2json(formSelector);
    document.cookie = 'first_name=' + encodeURIComponent(data['first_name']);
    document.cookie = 'last_name=' + encodeURIComponent(data['last_name']);
    document.cookie = 'org_name=' + encodeURIComponent(data['org_name']);
    document.cookie = 'department_name=' + encodeURIComponent(data['department_name']);
    document.cookie = 'industory=' + encodeURIComponent(data['industory']);
    document.cookie = 'industory_opt=' + encodeURIComponent(data['industory_opt']);
    document.cookie = 'position=' + encodeURIComponent(data['position']);
    document.cookie = 'job=' + encodeURIComponent(data['job']);
    document.cookie = 'role=' + encodeURIComponent(data['role']);
    document.cookie = 'grade=' + encodeURIComponent(data['grade']);
    url = $(formSelector).attr('action');
    console.log(url);
    item_ids = [];
    selected_items = get_selected_items();
    for (const [key, value] of Object.entries(selected_items)) {
      item_ids.push(value.id);
    }
    data.items = item_ids;
    console.log(data);
    data2api(url,'POST',data,function(data){
        console.log(data);
        if(data['result']=='NG'){
            for (const [key, value] of Object.entries(data['messages'])) {
                $('#target-create-messages').text($('#target-create-messages').text() + value);
                $('#target-create-messages').show();
            }
            for (const [key, value] of Object.entries(data['field_errors'])) {
                divname = '#feedback-' + key;
                inputname = '#target-' + key;
                $(inputname).addClass('is-invalid');
                for (idx = 0; idx < value.length; idx++) {
                $(divname).text($(divname).text()+value[idx]);
                }
            }
        } else {
            localStorage.removeItem('SELECTED_ITEMS')
            url = '/target/' + data['data']['uuid'];
            window.location.href = url;
        }
    },function(XMLHttpRequest, textStatus, errorThrown){
        alert(errorThrown);
    });

}