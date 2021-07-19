# Returns

- `Fold.collect([get_netbox_devices(), get_vni_data(CON)], IOSuccess(()))` <- acc must be representative of collected types
- Gotcha!  You can escape the "monad" by passing mutable references.

```python
def render_all(ext_data) -> t.Dict[str, ResultE[str]]:
    device_templates = {}
    devices = ext_data[0]
    for device in devices:
        get_device_ipam_data(CON, device["name"]).bind(
            lambda ipam: render_device_template(device, ipam, ext_data[1])
        ).map(lambda v: device_templates.update([(device["name"], v)]))
    return device_templates
```

- When using `Fold.collect`, is it a `Success` or `IOSuccess`?  ¯\_(ツ)_/¯  Use `pdb` to sort it out.