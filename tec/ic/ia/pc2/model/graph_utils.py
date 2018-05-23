import matplotlib.pyplot as plt


def show_graphics(result_list1, list1_tag,
                  result_list2, list2_tag,
                  common_tag):

    fig, axes = plt.subplots(2, sharex=True, figsize=(10, 5))
    fig.suptitle('Resultados')

    axes[0].set_ylabel(list1_tag, fontsize=12)
    axes[0].plot(result_list1)

    axes[1].set_ylabel(list2_tag, fontsize=12)
    axes[1].plot(result_list2)

    axes[1].set_xlabel(common_tag, fontsize=12)

    plt.show()


show_graphics(rl1, 'Mutación 40%',
              rl2, 'Mutación 80%',
              'Generaciones')
