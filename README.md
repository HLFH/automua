# automua: Email client configuration made easy

automua makes configuring email accounts easy. It unites methods for automated mailbox configuration from Apple's
[Mobileconfig](https://support.apple.com/en-gb/guide/profile-manager/pmdbd71ebc9/mac), Microsoft's
[Autodiscover](https://docs.microsoft.com/en-gb/exchange/architecture/client-access/autodiscover?view=exchserver-2019)
and Mozilla's [Autoconfig](https://hlfh.github.io/autoconfiguration/) in one tool.
automua is a fork of automx2. It accepts code contributions.

## Copyright
automua is a fork of [automx2](https://github.com/rseichter/automx2).
Check per-file copyright notices to see the sole modifications and the new files of the fork automua that are Copyright © 2022 Gaspard d'Hautefeuille.
automx2 and most of the files of the fork are Copyright © 2019-2022 Ralph Seichter.

automua is licensed under the GNU General Public License V3 or later. The project is hosted on GitHub in the [HLFH/automua](https://github.com/HLFH/automua) repository. It is published on [PyPI.org](https://pypi.org/project/automua/) and [Arch Linux AUR](https://aur.archlinux.org/packages/automua).

## Advantages
automua as a fork of automx2 has a few advantages:
 - automua is working [better with Autodiscover](https://github.com/HLFH/automua/issues/6) with modern Outlook clients such as *Outlook 2021 for Mac*;
 - automua implements [PEP 517 & PEP 518](https://github.com/HLFH/automua/issues/1) ;
 - automua supports [Arch Linux](https://aur.archlinux.org/packages/automua).

## Documentation

Detailed documentation is available in [HTML](https://hlfh.github.io/automua/),
[PDF](https://github.com/hlfh/automua/blob/master/docs/automua.pdf) and
[other formats](https://github.com/hlfh/automua/blob/master/docs).

## Dev notes

[Mobileconfig mail payload](https://support.apple.com/en-gb/guide/deployment/dep9c14bfc5/1/web/1.0)  
Use [Apple Configurator](https://apps.apple.com/app/apple-configurator-2/id1037126344) to go into details.

[MS-OXDSCLI Autodiscover Publishing and Lookup Protocol](https://learn.microsoft.com/en-us/openspecs/exchange_server_protocols/ms-oxdscli/78530279-d042-4eb0-a1f4-03b18143cd19)

Mozilla Thunderbird is looking up with [Autodiscover](https://github.com/mozilla/releases-comm-central/blob/master/mail/components/accountcreation/ExchangeAutoDiscover.jsm) before Autoconfig.  
But it [does not support the Encryption element](https://bugzilla.mozilla.org/show_bug.cgi?id=1799635), only the SSL element.


## Contributing

This project accepts code contributions.

Furthermore, submitting ideas, suggestions, requests and bug reports in the form of
[GitHub issues](https://github.com/hlfh/automua/issues) is welcome.

## Sponsorship

It is possible to sponsor specific new features. Please contact me via email to discuss this in detail.