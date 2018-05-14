# Get Notifications From The Chaos Toolkit Flow

The Chaos Toolkit generates events when it is executed. You may benefit from
those events to get notified via your chosen notification channels.

## Chaos Toolkit Flow Events

The Chaos Toolkit defines the following events:

Discovery flow

* `"discover-started"`: when the discovery flow has begun
* `"discover-completed"`: when the discovery flow has completed
* `"discover-failed"`: when the discovery flow has failed

Init flow

* `"init-started"`: when the init flow has begun
* `"init-completed"`: when the init flow has completed
* `"init-failed"`: when the init flow has failed

Run flow

* `"run-started"`: when the run flow has begun
* `"run-completed"`: when the run flow has completed
* `"run-failed"`: when the run flow has failed

Validate flow

* `"validate-started"`: when the validate flow has begun
* `"validate-completed"`: when the validate flow has completed
* `"validate-failed"`: when the validate flow has failed

## Declare Notification Channels

Notification channels are declared in the Chaos Toolkit
[settings file](cli.md#configure-the-chaos-toolkit) under the `notifications:`
section.

Here is an example:

```yaml
notifications:
 -
  type: http
  url: https://mystuff.com/api
  verify_tls: false
  headers:
    Authorization: "Bearer 1234"
 -
  type: plugin
  module: chaosslack.notification
  token: xop-1235
  channel: general
```

As you can see, channels are items in a list. Each channel is a mapping
describing the kind of channel and its required information.

For instance, here we have two channels. The first one is a call to the HTTPS
endpoint while the other one uses the [Chaos Toolkit Extension for Slack](sl)
to send messages to Slack channels.

[sl]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack

!!! warning
    Notification channels are run sequential to the whole chaos flow, so the
    more you declare, the bigger the impact they could have on the readibility
    of the experiment results.

### Filter Events

By default, all [events](#chaos-toolkit-flow-events) are sent to the channels.
However, you may decide, on a per channel basis, which events you want to be
sent. This is done by adding the `events` field to a channel:

```yaml
notifications:
 -
  type: plugin
  module: chaosslack.notification
  token: xop-1235
  channel: general
  events:
    - run-failed
```

The Slack channel will only receive events when a run experiment fails. This
is a list so declare as many events as you need.

### HTTP Notification Channel

A HTTP notification channel tells the Chaos Toolkit it must send the event
over HTTP (or HTTPS) to the given endpoint. Here is the description of its
fields:

- `type`: must `"http"` (required)
- `url`: the endpoint address (required)
- `verify_tls`: `true|false` depending if the endpoint certificates are
  self-signed
- `headers`: a mapping where the keys are header names and their associated
  values
- `forward_event_payload`: `true|false`. If `true`, the default, then the event
  payload is sent to that endpoint in a `POST` request. Otherwise, a `GET`
  request is performed with no body

### Plugin Notification Channel

A plugin notification channel is an integration between an external system and
the Chaos Toolkit event notification flow. It is more capable than basic HTTP
channels as they are fully fledged Python functions.

!!! warning
    A plugin channel could also be understood as a hook point into the Chaos
    Toolkit flow. Nothing prevents you from writing a plugin that performs
    operations based on those hook events. Please note however that they run
    sequentially to the whole flow, so the longer your operation takes, the
    longer it takes for your chaos experiment to carry on. This may invalidate
    certain experiments when timing is critical.

Here are the fields to declare one:

- `type`: must `"plugin"` (required)
- `module`: the dotted path to the Python module containing the function to
  apply (required)
- `func`: the name of the function to apply (in that module), defaults to
  `"notify"`

Any other fields will be passed on as-is to the function for its internal usage.
For instance:

```yaml
notifications:
 -
  type: plugin
  module: chaosslack.notification
  token: xop-1235
  channel: general
```

The `token` and `channel` fields will be provided directly to the `notify`
function of the `chaosslack.notification` module.

## Send Notifications To Slack

Notifying about Chaos Experiment in a slack channel is so common that we will
describe this integration here.

First, you must install the [Chaos Toolkit Integration for Slack][sl] as usual:

```console
(chaostk) $ pip install -U chaostoolkit-slack
```

Then, you should declare your notification channels as follows in the Chaos
Toolkit settings file.

```yaml
notifications:
 -
  type: plugin
  module: chaosslack.notification
  token: xop-1235
  channel: general
```

You may define as many channels as you need, for instance for different kind
of events.

The `token` and `channel` fields are mandatory in this case. The `token` field
must be set to a valid Slack token. You may start with a [legacy token][legtok]
before moving on to a [Slack App](slackapp) as per Slack [guidelines][].

[legtok]: https://api.slack.com/custom-integrations/legacy-tokens
[guidelines]: https://api.slack.com/docs/token-types
[slackapp]: https://api.slack.com/slack-apps

The Chaos Toolkit itself does not provide a Slack App at this moment.

The channel must be a name of an existing channel. The
payload message sent to Slack is defined in the [plugin][sl]. If you need to
amend it, please open an [issue][slissue] there.

[slissue]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack/issues

## Debugging Notifications

The Chaos Toolkit does its best to not break the experiment when an event
could not be pushed. If you do not see the notification you were expecting,
you should start investigating in the `chaostoolkit.og` file. Indeed, in that
case the error is logged at the `DEBUG` level with, hopefully, enough
information why the event could not be sent.

If the error occurs inside the core Chaos Toolkit library, please raise an
[issue there][chaoslibissues]. Otherwise, raise an issue with the appropriate
plugin.

[chaoslibissues]: https://github.com/chaostoolkit/chaostoolkit-lib/issues