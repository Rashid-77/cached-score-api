#!/usr/bin/env tarantool


local function init()
    link = box.schema.space.create('store')
    link:format({
             {name = 'key', type = 'string'},
             {name = 'value', type = 'string'},
             {name = 'ttl', type = 'number'},
    })

    link:create_index('primary', {
             type = 'hash',
             parts = {'key'}
             })
end


box.cfg{listen = 3301}
box.once('init', init)