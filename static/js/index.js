$(() => {
    // v2rayHas ?
    $.get('/v2rayHas', {}, (res) => {
        if (res['code'] == 0) 
            console.log('检查出错')
        else {
            $('#V2rayCorePath').val(res['data']['v2ray']['V2rayCorePath'])
            $('#V2rayLogPath').val(res['data']['v2ray']['V2rayLogPath'])
            $('#loglevel').text(res['data']['v2ray']['LogLevel'])
            $('#Port').val(res['data']['v2ray']['Port'])
            $('#Portocol').text(res['data']['v2ray']['Portocol'])
            $('#UUID').val(res['data']['v2ray']['UUID'])
            $('#Data_portocol').text(res['data']['v2ray']['DataPortocol'])

            if (res['data']['v2ray']['DataPortocol'] === "Shadowsocks")
                $('#Shadowsocks').fadeIn('fast', () => {
                    $('#ShadowsocksID').val(res['data']['shadowsocks']['ShadowsocksID'])
                    $('#ShadowsocksPwd').val(res['data']['shadowsocks']['ShadowsocksPwd'])
                })
        }
    })

    // 绑定下拉列表点击事件
    var dropdownitem = $('a.dropdown-item')
    for (var i = 0; i < dropdownitem.length; i++) {
        $(dropdownitem[i]).click(function() {
            droplistselected(this)
        })
    }

    $('#UuidUpdate').click(() => {
        updateUUID()
    })

    $('#SubmitConfig').click(() => {
        var a = ""
        if ($('#Data_portocol').text().replace(/\n/g, '').replace(/ /g, '') === "Shadowsocks")
            var shadowsocksres = updateShadowsocks()
            if (shadowsocksres == 1)
                a += "Shadowsocks配置更新成功\n"
            else a += "Shadowsocks配置更新失败\n"
        var configres = updateConfig()
        if (configres == 1)
            a += "V2ray配置更新成功"
        else a += "V2ray配置更新失败"
        alert(a)
    })
})

function droplistselected(t) {
    value = $(t).text()
    button = $(t).parent().parent().children()[0]
    $(button).text(value)
}

function updateUUID() {
    $.get('/updateUUID', {}, (res) => {
        if (res['code'] == 0)
            alert('无法获取UUID')
        else {
            $('#UUID').val(res['data']['uuid'])
        }
    })
}

function updateConfig() {
    var r = 0
    $.get('/updateConfig', {
        V2rayCorePath   : $('#V2rayCorePath').val(),
        V2rayLogPath    : $('#V2rayLogPath').val(),
        LogLevel        : $('#loglevel').text().replace(/\n/g, '').replace(/ /g, ''),
        Port            : $('#Port').val(),
        Portocol        : $('#Portocol').text().replace(/\n/g, '').replace(/ /g, ''),
        UUID            : $('#UUID').val(),
        DataPortocol    : $('#Data_portocol').text().replace(/\n/g, '').replace(/ /g, ''),
    }, (res) => {
        if (res['code'] == 1)
            r = 1
    })
    return r
}

function updateShadowsocks() {
    var r = 0
    $.get('/updateShadowsocks', {
        ShadowsocksID   : $('#ShadowsocksID').val(),
        ShadowsocksPwd  : $('#ShadowsocksPwd').val()
    }, (res) => {
        if (res['code'] == 1)
            r = 1
    })
    return r
}

function ShadowsocksConfig(t) {
    if ($(t).text() === "Vmess")
        $('#Shadowsocks').fadeOut('fast')
    else 
        $('#Shadowsocks').fadeIn('fast')
}