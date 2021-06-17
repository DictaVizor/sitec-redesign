$(window).on('load', function(){
    let subjectData
    //Subject units 8 max??
    const NUMBER_CLASS_NAME = {
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four',
        5: 'five',
        6: 'six',
        7: 'seven',
        8: 'eight'
    }

    let COLORS = ['blue', 'red', 'orange', 'violet', 'teal', 'olive', 'purple', 'brown', 'pink']


    let cycleAdvanceContainer = $('#cycle-advance-container')
    let studentDataContainer = $('#student-data-container')
    let exportScoresButton = $('button#export-scores')
    let exportScheduleButton = $('button#export-schedule')


    exportScoresButton.on('click', exportScores)
    exportScheduleButton.on('click', exportSchedule)


    cycleAdvanceContainer.api({
        on: 'now',
        action: 'get user profile',
        beforeXHR: suiSetRequestHeaders,
        onSuccess: function(response){
            subjectData = response.sitec_data.cycle_advance_data
            let studentData = response.sitec_data.panel_data
            $.each(subjectData, function(i, subject){
                let _subject = subjectTemplate(subject)
                cycleAdvanceContainer.append(_subject)
            })

            studentDataContainer.prepend(studentDataTemplate(studentData))

        }
    })






    function studentDataTemplate(data){
        let student = $(`
        <h3 class="ui header">
            ${data['current-period'].value}
         </h3>
        `)

        student.data = data
        return student
    }

    function subjectTemplate(data){
        let random = Math.floor(Math.random() * COLORS.length)
        let subject = $(`
            <div class="ui ${COLORS[random]} secondary inverted segment">
                <h3 class="ui header">
                <div class="content">
                    <strong>${data.name}</strong>
                        <div class="sub header">
                            ${data.title}
                        </div>
                    </div>
                </h3>  
                <div class="ui basic segment">
                    <div class="ui grid">
                        <div class="${NUMBER_CLASS_NAME[data.units.length]} column center aligned row unit headers">

                        </div>
                        <div class="sixteen wide column no padding">
                            <div class="ui inner segment">
                                <div class="ui grid">
                                    <div class="${NUMBER_CLASS_NAME[data.units.length]} column center aligned row unit scores">
                                            
                                    </div>
                                </div>
                                <div class="ui grid">
                                    <div class="${NUMBER_CLASS_NAME[data.units.length]} column center aligned row unit misses">
                                        
                                </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `)


        //add units
        $.each(data.units, function(i, unit){
            subject.find('.unit.headers').append(`
                <div class="column">
                    <span class="ui white text">U${unit.number+1}</span>
                </div>
            `)
            subject.find('.unit.scores').append(`
                <div class="ui column">
                <div class="ui white label">
                    ${unit.score}
                    </div>
                </div>
            `)
            subject.find('.unit.misses').append(`
                <div class="column">
                    <span class="ui small text">Faltas: ${unit.missed_days}</span>
                </div>
            `)
        })

        subject.data = data

        COLORS.splice($.inArray(COLORS[random], COLORS), 1)

        return subject
    }

    function exportSchedule(){
        console.log('Export Schedule!')
    }

    function exportScores(){
        console.log('Export scores!')
    }

})