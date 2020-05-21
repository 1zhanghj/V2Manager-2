$(() => {
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
        updateConfig()
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
    $.get('/updateConfig', {
        V2rayCorePath   : $('#V2rayCorePath').val(),
        V2rayLogPath    : $('#V2rayLogPath').val(),
        LogLevel        : $('#loglevel').text().replace(/\n/g, '').replace(/ /g, ''),
        Port            : $('#Port').val(),
        Portocol        : $('#Portocol').text().replace(/\n/g, '').replace(/ /g, ''),
        UUID            : $('#UUID').val(),
        DataPortocol    : $('#Data_portocol').text().replace(/\n/g, '').replace(/ /g, ''),
        ShadowsocksID   : $('#Data_portocol').text().replace(/\n/g, '').replace(/ /g, '') === 'Vmess' ? '' : $('#ShadowsocksID').val(),
        ShadowsocksPwd  : $('#Data_portocol').text().replace(/\n/g, '').replace(/ /g, '') === 'Vmess' ? '' : $('#ShadowsocksPwd').val()
    }, (res) => {
        if (res['code'] == 0)
            alert('V2ray配置更新失败')
        else {
            alert('V2ray配置已更新')
            window.location.reload()
        }
    })
}

function ShadowsocksConfig(t) {
    if ($(t).text() === "Vmess")
        $('#Shadowsocks').fadeOut('fast')
    else 
        $('#Shadowsocks').fadeIn('fast')
}

function V2rayControl(cmd) {
    $.get('/v2raycontrol', {
        cmd: cmd
    }, (res) => {
        console.log(res)
    })
}