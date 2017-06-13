.. highlight:: shell

============
Contributing
============


Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

To improve tracking of who did what, and to clarify the relationship
between the project and the contributor, we require a "sign-off" on patches
and pull requests submitted to this project. Instructions for how to do the
sign off are provided below.

Signing off certifies that you agree with the following:


Developer's Certificate of Origin 1.1
-------------------------------------


By making a contribution to this project, I certify that:

        (a) The contribution was created in whole or in part by me and I
            have the right to submit it under the open source license
            indicated in the file; or

        (b) The contribution is based upon previous work that, to the best
            of my knowledge, is covered under an appropriate open source
            license and I have the right under that license to submit that
            work with modifications, whether created in whole or in part
            by me, under the same open source license (unless I am
            permitted to submit under a different license), as indicated
            in the file; or

        (c) The contribution was provided directly to me by some other
            person who certified (a), (b) or (c) and I have not modified
            it.

        (d) I understand and agree that this project and the contribution
            are public and that a record of the contribution (including all
            personal information I submit with it, including my sign-off) is
            maintained indefinitely and may be redistributed consistent with
            this project or the open source license(s) involved.

To certify you agree with DCO, you will need to add the following line at
the end of each commit you submit to the project::

	Signed-off-by: Random J Developer <random@developer.example.org>

You must sign off with your real name as we unfortunately cannot accept
pseudonyms or anonymous contributions per this agreement.

You can do this easily in git by using ``-s`` when you run ``git commit``::
    $ git add .
    $ git commit -s -m "Your detailed description of your changes."


Automate the Sign Off
---------------------

To make integrating the sign-off in your commits easier, you can define a
git alias or you can create a local git hook.

By automating the sign off, you won't have to remember to use the "-s" flag
each time and risk a rejected Pull Request.


Git Alias
~~~~~~~~~

The easiest way to set this up is to create a git alias. While you can't
replace the "commit" command, you can make a command you'll remember to use::

    $ git config alias.sign "commit -s"


Git Hook
~~~~~~~~

The other way to automate the sign off is to write a git hook to populate
your commit message with the sign off text. The prepare-commit-msg hook is
the most straightforward option for adding the sign off to your commit
messages. Git provides sample files for each of these hooks in the
.git/hooks folder. Instructions are at the top explaining each of the
samples and how to activate the hook.

1. Open the prepare-commit-msg.sample and uncomment the last example::

    $ nano .git/hooks/prepare-commit-msg.sample

2. Activate the prepare-commit-msg hook by dropping the suffix::

    $ cp .git/hooks/prepare-commit-msg.sample .git/hooks/prepare-commit-msg
