"""
This example:
1. Connects to the current model
2. Deploy a charm and waits until it reports itself active
3. Destroys the unit and application
"""
from juju import errors
from juju import loop
from juju.model import Model

async def main():
    model = Model()
    print('Connecting to model')
    await model.connect()

    try:
        print('Deploying')
        application = await model.deploy(
            'cs:~karimsye/mariadb-k8s-charmed-osm-2',
            application_name='juju-qa-test2',
            channel='stable'
        )

        print('Second one Deploying')

        application = await model.deploy(
            'cs:~karimsye/mariadb-k8s-charmed-osm-2',
            application_name='juju-qa-test2',
            channel='stable'
        )

        print('Waiting for active')
        await model.block_until(
            lambda: all(unit.workload_status == 'active'
                        for unit in application.units))

    except errors.JujuError as e:
        if "already exists" in e.message:
            print(e.message)
        else:
            raise e
    finally:
        print('Disconnecting from model')
        await model.disconnect()

if __name__ == '__main__':
    loop.run(main())
