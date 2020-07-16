let cross_length = 10;
let radius;
let message = '';
let fill_bar_size = 0;
let show_probe_timer = false;

// main function used to display :
function play(disp_zone){
    display_fixation_cross(cross_length);
    if(disp_zone){
        display_game_zone(3, 9);
    }
    if(!paused){
        app.display_objects(mouseX, mouseY);
        app.check_collisions();
        app.move_objects();
        if(parameter_dict['gaming']!=0){
            if(parameter_dict['secondary_task']!='none'){
                sec_task.display_task();
            }
        }
        display_pannel();
        if(show_probe_timer){
            display_probe_timer();
        }
    }else{
        display_transition()
    }
}

function display_game_zone(){
    push();
    ellipseMode(CENTER);
    stroke('red');
    noFill();
    strokeWeight(4);
    radius = Math.round(ppd*max_angle);
    ellipse(windowWidth/2, windowHeight/2, radius);
    pop();
    push();
    ellipseMode(CENTER);
    stroke('red');
    noFill();
    strokeWeight(2);
    radius = Math.round(ppd*min_angle);
    ellipse(windowWidth/2, windowHeight/2, radius);
    pop();
}

function display_fixation_cross(cross_length){
    push();
    stroke('black');
    strokeWeight(2);
    rectMode(CENTER);
    fill(10,10,10,100);
    rect(windowWidth/2, windowHeight/2, cross_length, cross_length);
    pop();
}

function display_probe_timer(){

    // function called 60 times per second ==> probe_dur (in sec) * 60 == number of calls : nb_calls
    // [progress size = 300] / nb_calls == iter_size
    // fill_bar_size += iter_size
    if(fill_bar_size<300){
        fill_bar_size = fill_bar_size + (300/(parameter_dict['probe_time']*60))
    }
    push();
    textFont(gill_font_light);
    textSize(25);
    textStyle(BOLD);
    fill('white');
    textAlign(CENTER, TOP);
    rectMode(CORNERS);
    text("TEMPS RESTANT:", 70, 70, 200, 200);
    color('white');
    stroke(255);
    strokeWeight(3);
    noFill();
    rect(270,70,570,90);
    pop();
    push();
    fill('white');
    noStroke();
    rectMode(CORNERS);
    rect(270,70,270+fill_bar_size,90);
    pop();
}
function display_transition(){
    let trans_text = 'Great job, '+ str(parameter_dict['episode_number']) +' / 20' +' episode(s) have already been completed! \n'
        + 'You have found ' + str(parameter_dict['nb_target_retrieved'] + '/' + str(parameter_dict['n_targets']) + ' targets on last trial... \n')
        + 'Don\'t give up !';
    let width = 170;
    let height = 70;
    push();
    fill(250,250,250,210);
    rectMode(CENTER);
    rect(windowWidth/2, windowHeight/2, windowWidth, 500);
    button_keep.position(windowWidth/2 - width/2, windowHeight/2 + height/2);
    button_keep.size(width, height);
    button_keep.mousePressed(start_episode);
    textFont(gill_font_light);
    textSize(25);
    textStyle(BOLD);
    fill('black');
    textAlign(CENTER, TOP);
    rectMode(CORNERS);
    text(trans_text, 0, windowHeight/2 - height, windowWidth, 2*height);
    text(message, 0, windowHeight/2 - 2*height, windowWidth, height);
    pop();
}

// functions to parametrized game, timer and user interactions:
function start_episode(){
    message = '';
    fill_bar_size = 0;
    show_probe_timer = false;
    paused = false;
    button_keep.hide();
    button_hide_params.show();
    if(parameter_dict['episode_number']<20){
        console.log(parameter_dict);
        if(parameter_dict['debug']==1){
             app = new MOT(parameter_dict['n_targets'], parameter_dict['n_distractors'], Math.round(ppd*parameter_dict['angle_max']),
                  Math.round(ppd*parameter_dict['angle_min']), parameter_dict['radius'],parameter_dict['speed_max'],
                  parameter_dict['speed_max']);
        }else{
            if(parameter_dict['gaming']==0){
                console.log("no gaming mode");
                app = new MOT_Game_Light(parameter_dict['n_targets'], parameter_dict['n_distractors'], Math.round(ppd*parameter_dict['angle_max']),
                Math.round(ppd*parameter_dict['angle_min']), parameter_dict['radius'],parameter_dict['speed_max'],
                    parameter_dict['speed_max'], 'green', 'red');
            }else if(parameter_dict['gaming']==1){
                app = new MOT_Game(parameter_dict['n_targets'], parameter_dict['n_distractors'], Math.round(ppd*parameter_dict['angle_max']),
                Math.round(ppd*parameter_dict['angle_min']), parameter_dict['radius'],parameter_dict['speed_max'],
                    parameter_dict['speed_max'], goblin_image, guard_image);
                if(parameter_dict['secondary_task']!='none'){
                    sec_task = new Secondary_Task(leaf_image, parameter_dict['secondary_task'], parameter_dict['SRI_max']*1000,
                        parameter_dict['RSI']*1000, parameter_dict['tracking_time']*1000, parameter_dict['delta_orientation'],
                             app.all_objects)
                }
            }
        }
        app.change_target_color();
        // timer(app, 2000, 2000, 10000);
        timer(app, 1000*parameter_dict['presentation_time'],
            1000*parameter_dict['fixation_time'],
            1000*parameter_dict['tracking_time'],
            1000*parameter_dict['probe_time']);
        update_parameters_values();
        if(!hidden_pannel){
            show_inputs();
            switch_pannel_status();
        }
    }else{
        quit_game();
    }
}

function timer(app, presentation_time, fixation_time, tracking_time, probe_time){
    pres_timer = setTimeout(function () {
        // after presention_time ms
        // app.phase changes to fixation
        app.phase = 'fixation';
        app.frozen = true;
        // and stay in this frozen mode for fixation_time ms
        tracking_timer = setTimeout(function(){
            // after fixation_time ms
            // app.phase change to tracking mode
            if(parameter_dict['gaming']!=0 && parameter_dict['secondary_task']!='none') {
                sec_task.timer_pause();
            }
            app.phase = 'tracking';
            app.frozen = false;
            app.change_to_same_color();
            // and stay in this mode for tracking_time ms
           answer_timer = setTimeout(function(){
                // after tracking_time ms, app changes to answer phase
                app.phase = 'answer';
                app.frozen = true;
                app.enable_interact();
                show_answer_button();
                show_probe_timer = true;
                probe_timer = setTimeout(function () {
                    message = 'Temps écoulé!';
                    answer_button_clicked()
                },
                    probe_time)},
                tracking_time)},
            fixation_time)},
        presentation_time);
}

function show_answer_button(){
    button_answer = createButton('ANSWER');
    button_answer.position((windowWidth/2)-60, windowHeight - 0.07*windowHeight);
    button_answer.size(120,60);
    button_answer.mousePressed(answer_button_clicked);
}

function answer_button_clicked(){
    // reset few variables:
    fill_bar_size = 0;
    show_probe_timer = false;
    clearTimeout(probe_timer);
    button_answer.hide();
    let res = app.get_results();
    parameter_dict['nb_target_retrieved'] = res[0];
    parameter_dict['nb_distract_retrieved'] = res[1];
    if(parameter_dict['gaming']==1 && parameter_dict['secondary_task']!='none'){
        console.log("sec_task results", sec_task.results);
        parameter_dict['sec_task_results'] = JSON.stringify(sec_task.results);
    }
    app.phase = 'got_response';
    app.change_to_same_color();
    app.change_target_color();
    app.all_objects.forEach(function(item){item.interact_phase = false;});
    button_next_episode = createButton('NEXT EPISODE');
    button_next_episode.position((windowWidth/2)-60, windowHeight - 0.07*windowHeight);
    button_next_episode.size(120,60);
    button_next_episode.mousePressed(next_episode);
}

function next_episode(){
    button_next_episode.hide();
    // Send ajax request to backend:
    $.ajax({
    async: false,
    type: "POST",
    url: "/next_episode",
    dataType: "json",
    traditional: true,
    data: parameter_dict,
    success: function(data) {
        parameter_dict = data;
        }
    });
    paused = true;
    button_keep.show();
    hide_inputs();
    button_hide_params.hide();
}


