(function($){

    const COLORS = {
        'aprobada': 'inverted green',
        'pendiente': 'tertiary',
        'normal': '',
        'reprobada': 'inverted orange',
        'especial': 'inverted red',
        'sincursar': 'inverted secondary olive'
    }


    $.fn.kardexManager = function(settings){
        let self = this

        self.init = function(settings){
            self.settings = $.extend({}, settings, $.fn.kardexManager.settingsDefaults)
            self.subjects = []
            self.semesters = []
            self.loadData()


            return self
        }

        self.loadData = function(){
            self.api({
                on: 'now',
                action: 'get user profile',
                beforeXHR: suiSetRequestHeaders,
                onSuccess: function(response){
                    let data = response.sitec_data.kardex_data
                    self.processData(data)
                    self.trigger('data-loaded')
                },
                onError: function(){
                    //TODO: show error toast
                }
            })
        }

        self.processData = function(data){
            $.each(data, function(i, subject){
                self.addSubject(self.Subject(subject))
                self.semesters.push(subject.semester)
            })
            self.semesters = self.semesters.unique()
            self.loadSemesterSides()
        }

        self.loadSemesterSides = function(){
            $.each(self.semesters, function(i, semester){
                self.find('.sides').append(self.settings.semesterSideTemplate(semester))
            })
            self.find('.sides').children().first().toggleClass('active', true)

            self.shape = self.find('.shape').shape({
                onChange: function(){
                    self.updateSemesterFilter()
                }
            })
            self.find('.button.prev').on('click', function(){
                self.shape.shape('flip left')
            })
            self.find('.button.next').on('click', function(){
                self.shape.shape('flip right')
            })
            self.updateSemesterFilter()
        }

        self.updateSemesterFilter = function(){
            let semester = self.shape.find('.active').attr('data-semester')
            self.filterSubjectsBySemester(semester)
        }

        self.filterSubjectsBySemester = function(semester){
            $.each(self.subjects, function(i, subject){
                subject.toggle(subject.data.semester == semester)
            })
        }

        self.addSubject = function(subject){
            self.subjects.push(subject)
            self.find('.subject.segment').append(subject)
        }

        self.Subject = function(data){
            let subject = self.settings.subjectTemplate(data)

            subject.init = function(data){
                subject.data = data
                return subject
            }

            return subject.init(data)
        }

        return self.init(settings)
    }

    $.fn.kardexManager.settingsDefaults = {
        subjectTemplate: function(data){
            let segmentClass = COLORS[data.status]

            return $(`
                <div class="ui ${segmentClass} segment">
                    <p> <strong>Materia: </strong> ${data.name}</p>
                    <p> <strong>Codigo de Materia: </strong> ${data.slug}</p>
                </div>
            `)
        },
        semesterSideTemplate: function(number){
            return $(`
            <div class="ui header side" data-semester="${number}">Semestre ${number}</div>
            `)
        }
    }

})(jQuery)